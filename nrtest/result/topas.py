# -*- coding: utf-8 -*-

# third-party imports
from numpy.testing import assert_allclose
from topas2numpy import read_ntuple, BinnedResult

# project imports
from .factory import register, BaseResult


@register('topas binned')
class TopasBinnedResult(BaseResult, BinnedResult):
    def __init__(self, *args, **kwargs):
        BaseResult.__init__(self, *args, **kwargs)
        BinnedResult.__init__(self, self.path)

    def compatible(self, other, rtol, atol):
        try:
            assert self.quantity == other.quantity
            assert self.unit == other.unit
            assert set(self.statistics) == set(other.statistics)
            assert self.dimensions == other.dimensions
            for s in self.statistics:
                assert_allclose(self.data[s], other.data[s], rtol, atol)

        except AssertionError:
            return False
        else:
            return True


@register('topas ntuple')
class TopasNtupleResult(BaseResult):
    def __init__(self, *args, **kwargs):
        super(TopasNtupleResult, self).__init__(*args, **kwargs)
        self.data = read_ntuple(self.path)

    def compatible(self, other, rtol, atol):
        try:
            assert self.data.dtype.names == other.data.dtype.names
            assert self.data.size == other.data.size
            for s in self.data.dtype.names:
                assert_allclose(self.data[s], other.data[s], rtol, atol)

        except AssertionError:
            return False
        else:
            return True
