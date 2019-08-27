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
from os import path
from timer import Timer

import numpy as np
import pandas as pd
import torch.backends.cudnn as cudnn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data.distributed
import torchvision.models as models
from torch.utils.data import Dataset
from torchvision import transforms, datasets


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
_RGB_MEAN = [0.485, 0.456, 0.406]
_RGB_SD = [0.229, 0.224, 0.225]
_SEED = 42

# Settings from https://arxiv.org/abs/1706.02677.
_WARMUP_EPOCHS = 5
_WEIGHT_DECAY = 0.00005

_FAKE = _str_to_bool(os.getenv("FAKE", "False"))
_DATA_LENGTH = int(
    os.getenv("FAKE_DATA_LENGTH", 1281167)
)  # How much fake data to simulate, default to size of imagenet dataset
_DISTRIBUTED = _str_to_bool(os.getenv("DISTRIBUTED", "False"))

if _DISTRIBUTED:
    import horovod.torch as hvd


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


def _append_path_to(data_path, data_series):
    return data_series.apply(lambda x: path.join(data_path, x))


def _load_training(data_dir):
    logger = _get_logger()
    logger.info("Reading training data from {}".format(data_dir))
    train_df = pd.read_csv(path.join(data_dir, "train.csv"))
    return train_df.assign(
        filenames=_append_path_to(path.join(data_dir, "train"), train_df.filenames)
    )


def _load_validation(data_dir):
    logger = _get_logger()
    logger.info("Reading validation data from {}".format(data_dir))
    train_df = pd.read_csv(path.join(data_dir, "validation.csv"))
    return train_df.assign(
        filenames=_append_path_to(path.join(data_dir, "validation"), train_df.filenames)
    )


def _create_data_fn(train_path, test_path):
    train_df = _load_training(train_path)
    validation_df = _load_validation(test_path)
    # File-path
    train_X = train_df["filenames"].values
    validation_X = validation_df["filenames"].values
    # One-hot encoded labels for torch
    train_labels = train_df[["num_id"]].values.ravel()
    validation_labels = validation_df[["num_id"]].values.ravel()
    # Index starts from 0
    train_labels -= 1
    validation_labels -= 1
    return train_X, train_labels, validation_X, validation_labels


def _create_data(batch_size, num_batches, dim, channels, seed=42):
    np.random.seed(seed)
    return np.random.rand(batch_size * num_batches, channels, dim[0], dim[1]).astype(
        np.float32
    )


def _create_labels(batch_size, num_batches, n_classes):
    return np.random.choice(n_classes, batch_size * num_batches)


class FakeData(Dataset):
    def __init__(
        self,
        batch_size=32,
        num_batches=20,
        dim=(224, 224),
        n_channels=3,
        n_classes=10,
        length=_DATA_LENGTH,
        seed=42,
        data_transform=None,
    ):
        self.dim = dim
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.num_batches = num_batches
        self._data = _create_data(
            batch_size, self.num_batches, self.dim, self.n_channels
        )
        self._labels = _create_labels(batch_size, self.num_batches, self.n_classes)
        self.translation_index = np.random.choice(len(self._labels), length)
        self._length = length

        self._data_transform = data_transform
        logger = _get_logger()
        logger.info(
            "Creating fake data {} labels and {} images".format(
                n_classes, len(self._data)
            )
        )

    def __getitem__(self, idx):
        logger = _get_logger()
        logger.debug("Retrieving samples")
        logger.debug(str(idx))
        tr_index_array = self.translation_index[idx]

        if self._data_transform is not None:
            data = self._data_transform(self._data[tr_index_array])
        else:
            data = self._data[tr_index_array]

        return data, self._labels[tr_index_array]

    def __len__(self):
        return self._length


def _is_master(is_distributed=_DISTRIBUTED):
    if is_distributed:
        if hvd.rank() == 0:
            return True
        else:
            return False
    else:
        return True


def train(train_loader, model, criterion, optimizer, epoch):
    logger = _get_logger()
    msg = " duration({})  loss:{} total-samples: {}"
    t = Timer()
    t.start()
    logger.set_epoch(epoch)
    for i, (data, target) in enumerate(train_loader):
        data, target = data.cuda(non_blocking=True), target.cuda(non_blocking=True)
        optimizer.zero_grad()
        # compute output
        output = model(data)
        loss = criterion(output, target)
        # compute gradient and do SGD step
        loss.backward()
        optimizer.step()
        if i % 100 == 0:
            logger.info(msg.format(t.elapsed, loss.item(), i * len(data)))
            t.start()


def validate(train_loader, model, criterion):
    logger = _get_logger()
    msg = "validation duration({})  loss:{} total-samples: {}"
    t = Timer()
    t.start()
    model.eval()
    with torch.no_grad():
        for i, (data, target) in enumerate(train_loader):
            data, target = data.cuda(non_blocking=True), target.cuda(non_blocking=True)
            # compute output
            output = model(data)
            loss = criterion(output, target)
            # compute gradient and do SGD step
            if i % 100 == 0:
                logger.info(msg.format(t.elapsed, loss.item(), i * len(data)))
                t.start()


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


def _get_sampler(dataset, is_distributed=_DISTRIBUTED):
    if is_distributed:
        return torch.utils.data.distributed.DistributedSampler(
            dataset, num_replicas=hvd.size(), rank=hvd.rank()
        )
    else:
        return torch.utils.data.sampler.RandomSampler(dataset)


def main():
    logger = _get_logger()
    if _DISTRIBUTED:
        # Horovod: initialize Horovod.

        hvd.init()
        logger.info("Runnin Distributed")
        torch.manual_seed(_SEED)
        # Horovod: pin GPU to local rank.
        torch.cuda.set_device(hvd.local_rank())
        torch.cuda.manual_seed(_SEED)

    logger.info("PyTorch version {}".format(torch.__version__))

    if _FAKE:
        logger.info("Setting up fake loaders")
        train_dataset = FakeData(n_classes=1000, data_transform=torch.FloatTensor)
    else:
        normalize = transforms.Normalize(_RGB_MEAN, _RGB_SD)
        logger.info("Setting up loaders")
        train_dataset = datasets.ImageFolder(
            os.getenv("AZ_BATCHAI_INPUT_TRAIN"),
            transforms.Compose(
                [
                    transforms.RandomResizedCrop(_WIDTH),
                    transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    normalize,
                ]
            ),
        )

        validation_dataset = datasets.ImageFolder(
            os.getenv("AZ_BATCHAI_INPUT_TRAIN"),
            transforms.Compose(
                [
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    normalize,
                ]
            ),
        )

    train_sampler = _get_sampler(train_dataset)

    kwargs = {"num_workers": 5, "pin_memory": True}
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=_BATCHSIZE, sampler=train_sampler, **kwargs
    )

    # Autotune
    cudnn.benchmark = True

    logger.info("Loading model")
    # Load symbol
    model = models.__dict__["resnet50"](pretrained=False)

    model.cuda()

    if _DISTRIBUTED:
        # Horovod: broadcast parameters.
        hvd.broadcast_parameters(model.state_dict(), root_rank=0)

    num_gpus = hvd.size() if _DISTRIBUTED else 1
    # Horovod: scale learning rate by the number of GPUs.
    optimizer = optim.SGD(model.parameters(), lr=_LR * num_gpus, momentum=0.9)
    if _DISTRIBUTED:
        # Horovod: wrap optimizer with DistributedOptimizer.
        optimizer = hvd.DistributedOptimizer(
            optimizer, named_parameters=model.named_parameters()
        )

    criterion = F.cross_entropy

    if not _FAKE:
        val_sampler = _get_sampler(validation_dataset)
        val_loader = torch.utils.data.DataLoader(
            validation_dataset, batch_size=_BATCHSIZE, sampler=val_sampler, **kwargs
        )

    # Main training-loop
    logger.info("Training ...")
    for epoch in range(_EPOCHS):
        with Timer(output=logger.info, prefix="Training") as t:
            model.train()
            if _DISTRIBUTED:
                train_sampler.set_epoch(epoch)
            train(train_loader, model, criterion, optimizer, epoch)
        _log_summary(len(train_dataset), t.elapsed)

    if not _FAKE:
        validate(val_loader, model, criterion)


if __name__ == "__main__":
    main()
