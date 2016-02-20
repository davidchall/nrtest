# -*- coding: utf-8 -*-

# stores implementations and their aliases
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


def create(alias):
    """Retrieves a class from the registry.

        from nrtest.result import create
        result = create('default')('/path/to/file.txt')
    """
    return _registry.get(alias, _registry['default'])


class BaseResult(object):
    """Abstract base class for a result file."""
    def __init__(self, filepath):
        self.path = filepath

    def compatible(self, other, rtol, atol):
        raise NotImplementedError('abstract method')
