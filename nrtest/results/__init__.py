class Result(object):
    """Base class for test results, which defines the interface implemented by
    derived classes.
    """

    def compare(self, ref):
        """Compare to a reference result.

        Returns:
            max_delta: maximum relative difference between results
            avg_delta: mean relative difference between results
        """
        raise NotImplementedError('abstract method')
