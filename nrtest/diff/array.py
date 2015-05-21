import numpy as np

from .factory import register, NumericDiff, DiffException


@register('array')
class ArrayDiff(NumericDiff):

    def __init__(self, *args, **kwargs):
        super(ArrayDiff, self).__init__(*args, **kwargs)

        self.data_t = self._read_file(self.path_t)
        self.data_r = self._read_file(self.path_r)

        if self.data_t.shape != self.data_r.shape:
            raise DiffException('Inconsistent array shape')

        np.seterr(divide='ignore', invalid='ignore')
        self.diff = np.absolute((self.data_t - self.data_r) / self.data_r)
        both_zero_ind = np.nonzero((self.data_t == 0) & (self.data_r == 0))
        self.diff[both_zero_ind] = 0

    def _read_file(self, path):
        return np.loadtxt(path, ndmin=1)

    def max(self):
        return np.amax(self.diff)

    def min(self):
        return np.amin(self.diff)

    def mean(self):
        return np.mean(self.diff)


@register('csv')
class CsvDiff(ArrayDiff):

    def __init__(self, *args, **kwargs):
        super(CsvDiff, self).__init__(*args, **kwargs)

    def _read_file(self, path):
        return np.loadtxt(path, delimiter=',', ndmin=1)


@register('binarray')
class BinaryArrayDiff(ArrayDiff):

    def __init__(self, *args, **kwargs):
        super(BinaryArrayDiff, self).__init__(*args, **kwargs)

    def _read_file(self, path):
        return np.fromfile(path)
