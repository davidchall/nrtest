# -*- coding: utf-8 -*-

# project imports
from .factory import register, BaseResult


@register(None, 'none', 'null')
class NullResult(BaseResult):
    """A null result file. This is used when a result file is required to be
    produced by a test, but it is not possible to compare to a benchmark.
    """
    def __init__(self, *args, **kwargs):
        super(NullResult, self).__init__(*args, **kwargs)

    def compatible(self, other, rtol, atol):
        return True
