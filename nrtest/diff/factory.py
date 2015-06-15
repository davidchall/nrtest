from os.path import isfile


# stores implementations of BaseDiff and their aliases
_registry = {}


def register(*aliases):
    """Provides a decorator to add a class to the registry, under a number of
    aliases.
    """
    def wrap(cls):
        for alias in aliases:
            _registry[alias] = cls
        return cls
    return wrap


def factory(alias):
    """Retrieves a class from the registry.

        from nrtest.diff import factory
        diff = factory('default')('file1.txt', 'file2.txt')
    """
    return _registry.get(alias, _registry['default'])


class DiffException(Exception):
    """Raised if an error occurs during the diff (e.g. a file doesn't exist),
    or if the files are incomparable (e.g. arrays with different shapes).
    """
    pass


class BaseDiff(object):
    """Abstract base class that enables comparison of two result files.
    """
    def __init__(self, path_test, path_ref):
        if not isfile(path_test):
            raise DiffException('Unable to locate: "%s"' % path_test)
        if not isfile(path_ref):
            raise DiffException('Unable to locate: "%s"' % path_ref)

        self.path_t = path_test
        self.path_r = path_ref


class BooleanDiff(BaseDiff):

    numeric = False

    def __init__(self, *args, **kwargs):
        super(BooleanDiff, self).__init__(*args, **kwargs)

    def fail(self):
        raise NotImplementedError('abstract method')


class NumericDiff(BaseDiff):

    numeric = True

    def __init__(self, *args, **kwargs):
        super(NumericDiff, self).__init__(*args, **kwargs)

    def max(self):
        raise NotImplementedError('abstract method')

    def min(self):
        raise NotImplementedError('abstract method')

    def mean(self):
        raise NotImplementedError('abstract method')
