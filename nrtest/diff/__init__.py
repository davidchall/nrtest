import filecmp
from os.path import isfile


class DiffException(Exception):
    pass


class BaseDiff(object):
    """Base class that enables comparison of results.
    """
    def __init__(self, path_test, path_ref):
        """Args:
            path_test: path to result file under test
            path_ref:  path to reference result file
        """
        super(BaseDiff, self).__init__()

        if not isfile(path_test):
            raise DiffException('Unable to locate: "%s"' % path_test)
        if not isfile(path_ref):
            raise DiffException('Unable to locate: "%s"' % path_ref)

        self.path_t = path_test
        self.path_r = path_ref

    def max(self):
        raise NotImplementedError('abstract method')

    def min(self):
        raise NotImplementedError('abstract method')

    def mean(self):
        raise NotImplementedError('abstract method')

    def visual(self):
        raise NotImplementedError('abstract method')


class DefaultDiff(BaseDiff):
    """A default comparison of result files, which is similar to the command
    line utility `diff`.
    """
    def __init__(self, *args, **kwargs):
        super(DefaultDiff, self).__init__(*args, **kwargs)

        self.diff = filecmp.cmp(self.path_t, self.path_r)

    def max(self):
        return 0 if self.diff else 999.9

    def min(self):
        return self.max()

    def mean(self):
        return self.max()
