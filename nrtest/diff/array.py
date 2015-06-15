import numpy as np

from .factory import register, NumericDiff, DiffException


class ArrayDiff(NumericDiff):

    def __init__(self, is_binary, delimiter, compare_hist, *args, **kwargs):
        super(ArrayDiff, self).__init__(*args, **kwargs)

        self.is_binary = is_binary
        self.delimiter = delimiter
        self.compare_hist = compare_hist

        self.data_t = self._read_file(self.path_t)
        self.data_r = self._read_file(self.path_r)
        self.diff = None

        if compare_hist:
            if self.data_t.shape[1] != self.data_r.shape[1]:
                raise DiffException('Arrays have different number of columns')

            n_cols = self.data_t.shape[1]
            for iCol in range(n_cols):
                col_diff = self._compare_column(self.data_t[:, iCol],
                                                self.data_r[:, iCol])

                if self.diff is None:
                    self.diff = col_diff
                else:
                    self.diff = np.concatenate((self.diff, col_diff), axis=1)

            print self.diff

        else:
            self.diff = self._compare_array(self.data_t, self.data_r)

    def _read_file(self, path):
        if self.is_binary:
            return np.fromfile(path)
        else:
            return np.loadtxt(path, delimiter=self.delimiter, ndmin=1)

    def _compare_column(self, col_t, col_r):
        val_max = max(np.amax(col_t), np.amax(col_r))
        val_min = min(np.amin(col_t), np.amin(col_r))
        n_bins = 5

        hist_t, _ = np.histogram(col_t, bins=n_bins, range=(val_min, val_max),
                                 density=True)
        hist_r, _ = np.histogram(col_r, bins=n_bins, range=(val_min, val_max),
                                 density=True)

        hist_t = hist_t.reshape((-1, 1))
        hist_r = hist_r.reshape((-1, 1))

        return self._compare_array(hist_t, hist_r)

    def _compare_array(self, data_t, data_r):
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


@register('array')
def default(path_t, path_r):
    return ArrayDiff(False, None, True, path_t, path_r)


@register('csv')
def csv(path_t, path_r):
    return ArrayDiff(False, ',', False, path_t, path_r)


@register('binarray')
def binary(path_t, path_r):
    return ArrayDiff(True, None, False, path_t, path_r)
