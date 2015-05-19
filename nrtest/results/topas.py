import numpy as np
import logging

from nrtest.results import Result


class TopasScorer(Result):
    """docstring for TopasScorer"""
    def __init__(self):
        super(TopasScorer, self).__init__()

    @staticmethod
    def compare(path_test, path_ref):
        data_t = np.loadtxt(path_test, comments='#', delimiter=',', ndmin=1)
        data_r = np.loadtxt(path_ref, comments='#', delimiter=',', ndmin=1)

        # np.allclose(data_t, data_r, rtol=tolerance)

        if data_t.shape != data_r.shape:
            logging.debug('Inconsistent shapes')
            return 999, 999

        diff = (data_t - data_r) / data_r
        both_zero_ind = np.nonzero((data_t == 0) & (data_r == 0))
        diff[both_zero_ind] = 0

        return np.amax(diff), np.mean(diff)


class TopasPhaseSpace(Result):
    """docstring for TopasPhaseSpace"""
    def __init__(self):
        super(TopasScorer, self).__init__()

    @staticmethod
    def compare(path_test, path_ref):
        data_t = np.loadtxt(path_test, delimiter=None, ndmin=1)
        data_r = np.loadtxt(path_ref, delimiter=None, ndmin=1)

        # np.allclose(data_t, data_r, rtol=tolerance)

        if data_t.shape != data_r.shape:
            logging.debug('Inconsistent shapes')
            return 999, 999

        diff = (data_t - data_r) / data_r
        zero_indices = np.nonzero((data_t == 0) & (data_r == 0))
        diff[zero_indices] = 0

        return np.amax(diff), np.mean(diff)
