import numpy as np
import keras
import logging


def _get_logger():
    return logging.getLogger(__name__)

def _create_data(batch_size, num_batches, dim, channels, seed=42):
    np.random.seed(42)
    return np.random.rand(batch_size * num_batches,
                          dim[0],
                          dim[1],
                          channels).astype(np.float32)


def _create_labels(batch_size, num_batches, n_classes):
    return np.random.choice(n_classes, batch_size * num_batches)



class FakeDataGenerator(keras.preprocessing.image.Iterator):

    def __init__(self,
                 batch_size=32,
                 num_batches=20,
                 dim=(224, 224),
                 n_channels=3,
                 n_classes=10,
                 length=1000,
                 shuffle=True,
                 seed=42):

        'Initialization'
        super(FakeDataGenerator, self).__init__(length,
                                                batch_size,
                                                shuffle,
                                                seed)
        self.dim = dim
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.num_batches = num_batches
        self._data = _create_data(self.batch_size, self.num_batches, self.dim, self.n_channels)
        self._labels = _create_labels(self.batch_size, self.num_batches, self.n_classes)
        self.translation_index = np.random.choice(len(self._labels), length)


    def _get_batches_of_transformed_samples(self, index_array):
        logger = _get_logger()
        logger.debug('Retrieving samples')
        logger.debug(str(index_array))
        tr_index_array = self.translation_index[index_array]
        return self._data[tr_index_array], keras.utils.to_categorical(self._labels[tr_index_array], num_classes=self.n_classes)