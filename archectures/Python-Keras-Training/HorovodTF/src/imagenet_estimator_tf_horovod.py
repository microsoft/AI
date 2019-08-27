"""
Trains ResNet50 using Horovod.

It requires the following env variables
AZ_BATCHAI_INPUT_TRAIN
AZ_BATCHAI_INPUT_TEST
AZ_BATCHAI_OUTPUT_MODEL
AZ_BATCHAI_JOB_TEMP_DIR
"""
import glob
import logging
import os
import sys
from functools import lru_cache
from os import path
from pathlib import Path
from timer import Timer

import numpy as np
import tensorflow as tf
from resnet_model import resnet_v1
from toolz import pipe

_WIDTH = 224
_HEIGHT = 224
_CHANNELS = 3
_LR = 0.001
_EPOCHS = os.getenv("EPOCHS", 1)
_BATCHSIZE = 64
_R_MEAN = 123.68
_G_MEAN = 116.78
_B_MEAN = 103.94
_BUFFER = 256


def _str_to_bool(in_str):
    if "t" in in_str.lower():
        return True
    else:
        return False


_DISTRIBUTED = _str_to_bool(os.getenv("DISTRIBUTED", "False"))
_FAKE = _str_to_bool(os.getenv("FAKE", "False"))
_DATA_LENGTH = int(
    os.getenv("FAKE_DATA_LENGTH", 1281167)
)  # How much fake data to simulate, default to size of imagenet dataset
_VALIDATION = _str_to_bool(os.getenv("VALIDATION", "False"))

if _DISTRIBUTED:
    import horovod.tensorflow as hvd


tf_logger = logging.getLogger("tensorflow")
tf_logger.setLevel(logging.INFO)
stout = logging.StreamHandler(stream=sys.stdout)
tf_logger.addHandler(stout)


def _get_rank():
    if _DISTRIBUTED:
        try:
            return hvd.rank()
        except:
            return 0
    else:
        return 0


class HorovodAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        self._str_epoch = ""
        self._gpu_rank = 0
        super(HorovodAdapter, self).__init__(logger, {})

    def set_epoch(self, epoch):
        self._str_epoch = "[Epoch {}]".format(epoch)

    def process(self, msg, kwargs):
        kwargs["extra"] = {"gpurank": _get_rank(), "epoch": self._str_epoch}
        return msg, kwargs


@lru_cache()
def _get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "%(levelname)s:%(name)s:%(gpurank)d: %(epoch)s %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    adapter = HorovodAdapter(logger)
    return adapter


def _load_image(filename, channels=_CHANNELS):
    return tf.to_float(tf.image.decode_png(tf.read_file(filename), channels=channels))


def _resize(img, width=_WIDTH, height=_HEIGHT):
    return tf.image.resize_images(img, [height, width])


def _centre(img, mean_subtraction=(_R_MEAN, _G_MEAN, _B_MEAN)):
    return tf.subtract(img, list(mean_subtraction))


def _random_crop(img, width=_WIDTH, height=_HEIGHT, channels=_CHANNELS):
    return tf.random_crop(img, [height, width, channels])


def _random_horizontal_flip(img):
    return tf.image.random_flip_left_right(img)


def _preprocess_images(filename):
    return pipe(filename, _load_image, _resize, _centre)


def _preprocess_labels(label):
    return tf.cast(label, dtype=tf.int32)


def _transform_to_NCHW(img):
    return tf.transpose(img, [2, 0, 1])  # Transform from NHWC to NCHW


def _parse_function_train(tensor, label):
    img_rgb = pipe(tensor, _random_crop, _random_horizontal_flip, _transform_to_NCHW)

    return img_rgb, label


def _prep(filename, label):
    return tf.data.Dataset.from_tensor_slices(
        ([_preprocess_images(filename)], [_preprocess_labels(label)])
    )


def _parse_function_eval(filename, label):
    return (
        pipe(filename, _preprocess_images, _transform_to_NCHW),
        _preprocess_labels(label),
    )


def _get_optimizer(params, is_distributed=_DISTRIBUTED):
    if is_distributed:
        # Horovod: add Horovod Distributed Optimizer.
        return hvd.DistributedOptimizer(
            tf.train.MomentumOptimizer(
                learning_rate=params["learning_rate"] * hvd.size(), momentum=0.9
            )
        )
    else:
        return tf.train.MomentumOptimizer(
            learning_rate=params["learning_rate"], momentum=0.9
        )


def build_network(features, mode, params):
    network = resnet_v1(
        resnet_depth=50, num_classes=params["classes"], data_format="channels_first"
    )
    return network(inputs=features, is_training=(mode == tf.estimator.ModeKeys.TRAIN))


def model_fn(features, labels, mode, params):
    """
    features: This is the x-arg from the input_fn.
    labels:   This is the y-arg from the input_fn,
              see e.g. train_input_fn for these two.
    mode:     Either TRAIN, EVAL, or PREDICT
    params:   User-defined hyper-parameters, e.g. learning-rate.
    """
    logger = _get_logger()
    logger.info("Creating model in {} mode".format(mode))

    logits = build_network(features, mode, params)

    if mode == tf.estimator.ModeKeys.PREDICT:
        # Softmax output of the neural network.
        y_pred = tf.nn.softmax(logits=logits)

        # Classification output of the neural network.
        y_pred_cls = tf.argmax(y_pred, axis=1)

        predictions = {
            "class_ids": y_pred_cls,
            "probabilities": y_pred,
            "logits": logits,
        }
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits=logits, labels=labels
    )
    loss = tf.reduce_mean(cross_entropy)

    if mode == tf.estimator.ModeKeys.EVAL:
        # Softmax output of the neural network.
        y_pred = tf.nn.softmax(logits=logits)

        # Classification output of the neural network.
        y_pred_cls = tf.argmax(y_pred, axis=1)

        accuracy = tf.metrics.accuracy(
            labels=tf.argmax(labels, axis=1), predictions=y_pred_cls, name="acc_op"
        )
        metrics = {"accuracy": accuracy}
        tf.summary.scalar("accuracy", accuracy[1])
        return tf.estimator.EstimatorSpec(mode=mode, eval_metric_ops=metrics, loss=loss)

    optimizer = _get_optimizer(params)

    train_op = optimizer.minimize(loss=loss, global_step=tf.train.get_global_step())

    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)


def _append_path_to(data_path, data_series):
    return data_series.apply(lambda x: path.join(data_path, x))


def _load_training(data_dir):
    return list(glob.glob(Path(data_dir) / "**" / "*.jpg"))


def _load_validation(data_dir):
    return list(glob.glob(Path(data_dir) / "**" / "*.jpg"))


def _create_data_fn(train_path, test_path):
    logger = _get_logger()
    logger.info("Reading training data info")
    train_df = _load_training(train_path)

    logger.info("Reading validation data info")
    validation_df = _load_validation(test_path)

    train_labels = train_df[["num_id"]].values.ravel() - 1
    validation_labels = validation_df[["num_id"]].values.ravel() - 1

    train_data = tf.data.Dataset.from_tensor_slices(
        (train_df["filenames"].values, train_labels)
    )
    train_data_transform = tf.contrib.data.map_and_batch(
        _parse_function_train, _BATCHSIZE, num_parallel_batches=5
    )
    train_data = train_data.apply(
        tf.contrib.data.parallel_interleave(
            _prep, cycle_length=5, buffer_output_elements=1024
        )
    )

    train_data = (
        train_data.shuffle(1024).repeat().apply(train_data_transform).prefetch(_BUFFER)
    )

    validation_data = tf.data.Dataset.from_tensor_slices(
        (validation_df["filenames"].values, validation_labels)
    )
    validation_data_transform = tf.contrib.data.map_and_batch(
        _parse_function_eval, _BATCHSIZE, num_parallel_batches=4
    )
    validation_data = validation_data.apply(validation_data_transform).prefetch(_BUFFER)

    def _train_input_fn():
        return train_data.make_one_shot_iterator().get_next()

    def _validation_input_fn():
        return validation_data.make_one_shot_iterator().get_next()

    _train_input_fn.length = len(train_df)
    _validation_input_fn.length = len(validation_df)
    _train_input_fn.classes = 1000
    _validation_input_fn.classes = 1000

    return _train_input_fn, _validation_input_fn


def _create_data(batch_size, num_batches, dim, channels, seed=42):
    np.random.seed(seed)
    return np.random.rand(batch_size * num_batches, channels, dim[0], dim[1]).astype(
        np.float32
    )


def _create_labels(batch_size, num_batches, n_classes):
    return np.random.choice(n_classes, batch_size * num_batches)


def _create_fake_data_fn(train_length=_DATA_LENGTH, valid_length=50000, num_batches=40):
    """ Creates fake dataset

    Data is returned in NCHW since this tends to be faster on GPUs
    """
    logger = _get_logger()
    logger.info("Creating fake data")

    data_array = _create_data(_BATCHSIZE, num_batches, (_HEIGHT, _WIDTH), _CHANNELS)
    labels_array = _create_labels(_BATCHSIZE, num_batches, 1000)

    def fake_data_generator():
        for i in range(num_batches):
            yield data_array[i * _BATCHSIZE : (i + 1) * _BATCHSIZE], labels_array[
                i * _BATCHSIZE : (i + 1) * _BATCHSIZE
            ]

    train_data = tf.data.Dataset().from_generator(
        fake_data_generator,
        output_types=(tf.float32, tf.int32),
        output_shapes=(
            tf.TensorShape([None, _CHANNELS, _HEIGHT, _WIDTH]),
            tf.TensorShape([None]),
        ),
    )

    train_data = train_data.shuffle(40 * _BATCHSIZE).repeat().prefetch(_BUFFER)

    validation_data = tf.data.Dataset().from_generator(
        fake_data_generator,
        output_types=(tf.float32, tf.int32),
        output_shapes=(
            tf.TensorShape([None, _CHANNELS, _HEIGHT, _WIDTH]),
            tf.TensorShape([None]),
        ),
    )

    validation_data = validation_data.prefetch(_BUFFER)

    def _train_input_fn():
        return train_data.make_one_shot_iterator().get_next()

    def _validation_input_fn():
        return validation_data.make_one_shot_iterator().get_next()

    _train_input_fn.length = train_length
    _validation_input_fn.length = valid_length
    _train_input_fn.classes = 1000
    _validation_input_fn.classes = 1000

    return _train_input_fn, _validation_input_fn


def _get_runconfig(is_distributed=_DISTRIBUTED):
    if is_distributed:
        # Horovod: pin GPU to be used to process local rank (one GPU per process)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.gpu_options.visible_device_list = str(hvd.local_rank())

        return tf.estimator.RunConfig(
            save_checkpoints_steps=None,
            save_checkpoints_secs=None,
            session_config=config,
        )
    else:
        return tf.estimator.RunConfig(save_checkpoints_steps=None)


def _get_model_dir(is_distributed=_DISTRIBUTED):
    if is_distributed:
        # Horovod: save checkpoints only on worker 0 to prevent other workers from
        # corrupting them.
        return (
            os.getenv("AZ_BATCHAI_OUTPUT_MODEL")
            if hvd.rank() == 0
            else os.getenv("AZ_BATCHAI_JOB_TEMP_DIR")
        )
    else:
        return os.getenv("AZ_BATCHAI_OUTPUT_MODEL")


def _get_hooks(is_distributed=_DISTRIBUTED):
    logger = _get_logger()
    if is_distributed:
        bcast_hook = hvd.BroadcastGlobalVariablesHook(0)
        logger.info("Rank: {} Cluster Size {}".format(hvd.local_rank(), hvd.size()))
        return [bcast_hook]
    else:
        return []


def _is_master(is_distributed=_DISTRIBUTED):
    if is_distributed:
        if hvd.rank() == 0:
            return True
        else:
            return False
    else:
        return True


def _log_summary(data_length, duration):
    logger = _get_logger()
    images_per_second = data_length / duration
    logger.info("Data length:      {}".format(data_length))
    logger.info("Total duration:   {:.3f}".format(duration))
    logger.info("Total images/sec: {:.3f}".format(images_per_second))
    logger.info(
        "Batch size:       (Per GPU {}: Total {})".format(
            _BATCHSIZE, hvd.size() * _BATCHSIZE if _DISTRIBUTED else _BATCHSIZE
        )
    )
    logger.info("Distributed:      {}".format("True" if _DISTRIBUTED else "False"))
    logger.info("Num GPUs:         {:.3f}".format(hvd.size() if _DISTRIBUTED else 1))
    logger.info("Dataset:          {}".format("Synthetic" if _FAKE else "Imagenet"))


def main():

    if _DISTRIBUTED:
        # Horovod: initialize Horovod.
        hvd.init()
        logger = _get_logger()
        logger.info("Runnin Distributed")
    else:
        logger = _get_logger()

    logger.info("Tensorflow version {}".format(tf.__version__))
    if _FAKE:
        train_input_fn, validation_input_fn = _create_fake_data_fn()
    else:
        train_input_fn, validation_input_fn = _create_data_fn(
            os.getenv("AZ_BATCHAI_INPUT_TRAIN"), os.getenv("AZ_BATCHAI_INPUT_TEST")
        )

    run_config = _get_runconfig()
    model_dir = _get_model_dir()

    params = {"learning_rate": _LR, "classes": train_input_fn.classes}
    logger.info("Creating estimator with params: {}".format(params))
    model = tf.estimator.Estimator(
        model_fn=model_fn, params=params, model_dir=model_dir, config=run_config
    )

    hooks = _get_hooks()
    num_gpus = hvd.size() if _DISTRIBUTED else 1
    with Timer(output=logger.info, prefix="Training") as t:
        logger.info("Training...")
        model.train(
            input_fn=train_input_fn,
            steps=_EPOCHS * train_input_fn.length // (_BATCHSIZE * num_gpus),
            hooks=hooks,
        )

    _log_summary(_EPOCHS * train_input_fn.length, t.elapsed)

    if _is_master() and _FAKE is False and _VALIDATION:
        with Timer(output=logger.info, prefix="Testing"):
            logger.info("Testing...")
            model.evaluate(input_fn=validation_input_fn)


if __name__ == "__main__":
    main()
