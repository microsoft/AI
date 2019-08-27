"""
Trains ResNet50 in Keras using Horovod.

It requires the following env variables
AZ_BATCHAI_INPUT_TRAIN
AZ_BATCHAI_INPUT_TEST
AZ_BATCHAI_OUTPUT_MODEL
AZ_BATCHAI_JOB_TEMP_DIR
"""
import logging
import os
import sys
from functools import lru_cache
from timer import Timer

import keras
import tensorflow as tf
from data_generator import FakeDataGenerator
from keras import backend as K
from keras.preprocessing import image


def _str_to_bool(in_str):
    if "t" in in_str.lower():
        return True
    else:
        return False


_WIDTH = 224
_HEIGHT = 224
_CHANNELS = 3
_LR = 0.001
_EPOCHS = os.getenv("EPOCHS", 1)
_BATCHSIZE = 64
_R_MEAN = 123.68
_G_MEAN = 116.78
_B_MEAN = 103.94

# Settings from https://arxiv.org/abs/1706.02677.
_WARMUP_EPOCHS = 5
_WEIGHT_DECAY = 0.00005

_NUM_WORKERS = int(os.getenv("NUM_WORKERS", 10))
_MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", 10))
_MULTIPROCESSING = _str_to_bool(os.getenv("MULTIPROCESSING", "False"))
_DISTRIBUTED = _str_to_bool(os.getenv("DISTRIBUTED", "False"))
_FAKE = _str_to_bool(os.getenv("FAKE", "False"))
_DATA_LENGTH = int(
    os.getenv("FAKE_DATA_LENGTH", 1281167)
)  # How much fake data to simulate, default to size of imagenet dataset
_VALIDATION = _str_to_bool(os.getenv("VALIDATION", "False"))


if _DISTRIBUTED:
    import horovod.keras as hvd


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


def _create_model():
    logger = _get_logger()
    logger.info("Creating model")
    # Set up standard ResNet-50 model.
    model = keras.applications.resnet50.ResNet50(weights=None)
    # ResNet-50 model that is included with Keras is optimized for inference.
    # Add L2 weight decay & adjust BN settings.
    model_config = model.get_config()
    for layer, layer_config in zip(model.layers, model_config["layers"]):
        if hasattr(layer, "kernel_regularizer"):
            regularizer = keras.regularizers.l2(_WEIGHT_DECAY)
            layer_config["config"]["kernel_regularizer"] = {
                "class_name": regularizer.__class__.__name__,
                "config": regularizer.get_config(),
            }
        if type(layer) == keras.layers.BatchNormalization:
            layer_config["config"]["momentum"] = 0.9
            layer_config["config"]["epsilon"] = 1e-5
    model = keras.models.Model.from_config(model_config)
    return model


def _validation_data_iterator_from():
    # Validation data iterator.

    test_gen = image.ImageDataGenerator(
        zoom_range=(0.875, 0.875),
        preprocessing_function=keras.applications.resnet50.preprocess_input,
    )
    test_iter = test_gen.flow_from_directory(
        os.getenv("AZ_BATCHAI_INPUT_TEST"),
        batch_size=_BATCHSIZE,
        target_size=(224, 224),
    )
    return test_iter


def _training_data_iterator_from():
    # Training data iterator.
    train_gen = image.ImageDataGenerator(
        width_shift_range=0.33,
        height_shift_range=0.33,
        zoom_range=0.5,
        horizontal_flip=True,
        preprocessing_function=keras.applications.resnet50.preprocess_input,
    )
    train_iter = train_gen.flow_from_directory(
        os.getenv("AZ_BATCHAI_INPUT_TRAIN"),
        batch_size=_BATCHSIZE,
        target_size=(224, 224),
    )
    return train_iter


def _fake_data_iterator_from(length=_DATA_LENGTH):
    return FakeDataGenerator(batch_size=_BATCHSIZE, n_classes=1000, length=length)


def _get_optimizer(params, is_distributed=_DISTRIBUTED):
    if is_distributed:
        # Horovod: adjust learning rate based on number of GPUs.
        opt = keras.optimizers.SGD(
            lr=params["learning_rate"] * hvd.size(), momentum=params["momentum"]
        )
        # Horovod: add Horovod Distributed Optimizer.
        return hvd.DistributedOptimizer(opt)
    else:
        return keras.optimizers.SGD(
            lr=params["learning_rate"], momentum=params["momentum"]
        )


def _get_runconfig(is_distributed=_DISTRIBUTED):
    if is_distributed:
        # Horovod: pin GPU to be used to process local rank (one GPU per process)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.gpu_options.visible_device_list = str(hvd.local_rank())
    else:
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
    return config


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


def _get_hooks(is_distributed=_DISTRIBUTED, verbose=1):
    logger = _get_logger()
    if is_distributed:
        logger.info("Rank: {} Cluster Size {}".format(hvd.local_rank(), hvd.size()))
        return [
            # Horovod: broadcast initial variable states from rank 0 to all other processes.
            # This is necessary to ensure consistent initialization of all workers when
            # training is started with random weights or restored from a checkpoint.
            hvd.callbacks.BroadcastGlobalVariablesCallback(0),
            # Horovod: average metrics among workers at the end of every epoch.
            #
            # Note: This callback must be in the list before the ReduceLROnPlateau,
            # TensorBoard, or other metrics-based callbacks.
            hvd.callbacks.MetricAverageCallback(),
            # Horovod: using `lr = 1.0 * hvd.size()` from the very beginning leads to worse final
            # accuracy. Scale the learning rate `lr = 1.0` ---> `lr = 1.0 * hvd.size()` during
            # the first five epochs. See https://arxiv.org/abs/1706.02677 for details.
            hvd.callbacks.LearningRateWarmupCallback(
                warmup_epochs=_WARMUP_EPOCHS, verbose=verbose
            ),
            # Horovod: after the warmup reduce learning rate by 10 on the 30th, 60th and 80th epochs.
            hvd.callbacks.LearningRateScheduleCallback(
                start_epoch=_WARMUP_EPOCHS, end_epoch=30, multiplier=1.0
            ),
            hvd.callbacks.LearningRateScheduleCallback(
                start_epoch=30, end_epoch=60, multiplier=1e-1
            ),
            hvd.callbacks.LearningRateScheduleCallback(
                start_epoch=60, end_epoch=80, multiplier=1e-2
            ),
            hvd.callbacks.LearningRateScheduleCallback(start_epoch=80, multiplier=1e-3),
        ]
    else:
        return []


class LoggerCallback(keras.callbacks.Callback):
    def __init__(self, logger, data_length):
        self._timer = Timer(
            output=logger.info, prefix="Epoch duration: ", fmt="{:.3f} seconds"
        )
        self._data_length = data_length

    def on_epoch_begin(self, epoch, logs):
        logger = _get_logger()
        logger.set_epoch(epoch)
        self._timer.start()

    def on_epoch_end(self, epoch, logs):
        duration = self._timer.elapsed
        _log_summary(self._data_length, duration)


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
    verbose = 1
    logger = _get_logger()
    if _DISTRIBUTED:
        # Horovod: initialize Horovod.
        hvd.init()
        logger.info("Runnin Distributed")
        verbose = 1 if hvd.rank() == 0 else 0

    logger.info("Tensorflow version {}".format(tf.__version__))
    K.set_session(tf.Session(config=_get_runconfig()))

    # Horovod: broadcast resume_from_epoch from rank 0 (which will have
    # checkpoints) to other ranks.
    resume_from_epoch = 0
    if _DISTRIBUTED:
        resume_from_epoch = hvd.broadcast(
            resume_from_epoch, 0, name="resume_from_epoch"
        )

    if _FAKE:
        train_iter = _fake_data_iterator_from()
    else:
        train_iter = _training_data_iterator_from()
        test_iter = _validation_data_iterator_from() if _VALIDATION else None

    model = _create_model()

    params = {"learning_rate": _LR, "momentum": 0.9}

    opt = _get_optimizer(params)
    model.compile(
        loss=keras.losses.categorical_crossentropy,
        optimizer=opt,
        metrics=["accuracy", "top_k_categorical_accuracy"],
    )

    model_dir = _get_model_dir()
    checkpoint_format = os.path.join(model_dir, "checkpoint-{epoch}.h5")

    callbacks = _get_hooks()
    callbacks.append(LoggerCallback(logger, len(train_iter) * _BATCHSIZE))

    # Horovod: save checkpoints only on the first worker to prevent other workers from corrupting them.
    if _is_master():
        callbacks.append(keras.callbacks.ModelCheckpoint(checkpoint_format))
        # callbacks.append(keras.callbacks.TensorBoard(log_dir))

    # Restore from a previous checkpoint, if initial_epoch is specified.
    # Horovod: restore on the first worker which will broadcast weights to other workers.
    if resume_from_epoch > 0 and _is_master():
        model.load_weights(checkpoint_format.format(epoch=resume_from_epoch))

    logger.info("Training...")
    # Train the model. The training will randomly sample 1 / N batches of training data and
    # 3 / N batches of validation data on every worker, where N is the number of workers.
    # Over-sampling of validation data helps to increase probability that every validation
    # example will be evaluated.
    num_workers = hvd.size() if _DISTRIBUTED else 1
    model.fit_generator(
        train_iter,
        steps_per_epoch=len(train_iter) // num_workers,
        callbacks=callbacks,
        epochs=_EPOCHS,
        verbose=verbose,
        workers=_NUM_WORKERS,
        max_queue_size=_MAX_QUEUE_SIZE,
        use_multiprocessing=_MULTIPROCESSING,
        initial_epoch=resume_from_epoch,
    )

    if _FAKE is False and _VALIDATION:
        # Evaluate the model on the full data set.
        with Timer(output=logger.info, prefix="Testing"):
            logger.info("Testing...")
            score = hvd.allreduce(
                model.evaluate_generator(test_iter, len(test_iter), workers=10)
            )
            if verbose:
                print("Test loss:", score[0])
            print("Test accuracy:", score[1])


if __name__ == "__main__":
    main()
