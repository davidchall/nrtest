# -*- coding: utf-8 -*-

# system imports
import filecmp

# project imports
from .factory import register, BaseResult


@register('default', 'text')
class DefaultResult(BaseResult):
    """A default result file, which can be compared in a similar fashion
    to the diff utility.
    """
    def __init__(self, *args, **kwargs):
        super(DefaultResult, self).__init__(*args, **kwargs)

    def compatible(self, other, rtol, atol):
        return filecmp.cmp(self.path, other.path, shallow=False)
