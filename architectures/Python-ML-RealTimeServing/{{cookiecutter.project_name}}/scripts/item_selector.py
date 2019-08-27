# From: http://scikit-learn.org/0.18/auto_examples/hetero_feature_union.html
from sklearn.base import BaseEstimator, TransformerMixin


class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at provided
    key(s).

    The data are expected to be stored in a 2D data structure, where
    the first index is over features and the second is over samples,
    i.e.

    >> len(data[keys]) == n_samples

    Please note that this is the opposite convention to scikit-learn
    feature matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[keys]).  Examples include: a dict of lists, 2D numpy array,
    Pandas DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
               'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample
    (e.g. a list of dicts).  If your data are structured this way,
    consider a transformer along the lines of
    `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    keys : hashable or list of hashable, required
        The key(s) corresponding to the desired value(s) in a mappable.

    """

    def __init__(self, keys):
        if type(keys) is list:
            if any([getattr(key, '__hash__', None) is None for key in keys]):
                raise TypeError('Not all keys are hashable')
        elif getattr(keys, '__hash__', None) is None:
            raise TypeError('keys is not hashable')
        self.keys = keys

    def fit(self, x, *args, **kwargs):
        if type(self.keys) is list:
            if not all([key in x for key in self.keys]):
                raise KeyError('Not all keys in data')
        elif self.keys not in x:
            raise KeyError('key not in data')
        return self

    def transform(self, data_dict, *args, **kwargs):
        return data_dict[self.keys]

    def get_feature_names(self):
        return self.keys
