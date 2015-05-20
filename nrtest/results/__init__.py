class ResultDiffException(Exception):
    pass


class ResultDiff(object):
    """Base class that enables comparison of test results."""
    def __init__(self, path_test, path_ref):
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
