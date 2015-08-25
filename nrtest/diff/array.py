# third party imports
import numpy as np

# project imports
from .factory import register, NumericDiff, DiffException


class ArrayDiff(NumericDiff):

    def __init__(self, is_binary, delimiter, *args, **kwargs):
        super(ArrayDiff, self).__init__(*args, **kwargs)

        self.is_binary = is_binary
        self.delimiter = delimiter

        self.data_t = self._read_file(self.path_t)
        self.data_r = self._read_file(self.path_r)

        self.diff = self._compare(self.data_t, self.data_r)

    def _read_file(self, path):
        if self.is_binary:
            return np.fromfile(path)
        else:
            return np.loadtxt(path, delimiter=self.delimiter, ndmin=1)

    def _compare(self, data_t, data_r):
        if data_t.shape != data_r.shape:
            raise DiffException('Inconsistent array shape')

        np.seterr(divide='ignore', invalid='ignore')
        diff = np.absolute((data_t - data_r) / data_r)
        both_zero_ind = np.nonzero((data_t == 0) & (data_r == 0))
        diff[both_zero_ind] = 0

        return diff

    def max(self):
        return np.amax(self.diff)

    def min(self):
        return np.amin(self.diff)

    def mean(self):
        return np.mean(self.diff)


class NtupleDiff(ArrayDiff):

    def __init__(self, is_binary, delimiter, *args, **kwargs):
        super(NtupleDiff, self).__init__(is_binary, delimiter, *args, **kwargs)

    def _compare(self, data_t, data_r):
        n_cols = data_t.shape[1]
        if data_r.shape[1] != n_cols:
            raise DiffException('Arrays have different number of columns')

        mean_t = np.mean(data_t, axis=0)
        mean_r = np.mean(data_r, axis=0)
        mean_diff = ArrayDiff._compare(self, mean_t, mean_r)

        std_t = np.std(data_t, axis=0)
        std_r = np.std(data_r, axis=0)
        std_diff = ArrayDiff._compare(self, std_t, std_r)

        return np.vstack((mean_diff, std_diff))


@register('array')
def default(path_t, path_r):
    return ArrayDiff(False, None, path_t, path_r)


@register('csv_array')
def csv(path_t, path_r):
    return ArrayDiff(False, ',', path_t, path_r)


@register('bin_array')
def binary(path_t, path_r):
    return ArrayDiff(True, None, path_t, path_r)


@register('ntuple')
def ntuple(path_t, path_r):
    return NtupleDiff(False, None, path_t, path_r)


@register('csv_ntuple')
def csv(path_t, path_r):
    return NtupleDiff(False, ',', path_t, path_r)


# does not yet work, since we don't know n_columns
@register('bin_ntuple')
def binary(path_t, path_r):
    return NtupleDiff(True, None, path_t, path_r)
