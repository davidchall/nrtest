from nrtest.results import Result


class DurationResult(Result):
    """A result storing the test execution time."""
    def __init__(self, duration):
        """Initializes a new instance of the DurationResult class.

        Args:
            duration: test execution time in seconds
        """
        super(DurationResult, self).__init__()
        self.duration = duration

    def compare(self, ref):
        """Compare to a reference result. The comparison is one-sided because
        only an increase in duration is considered a failure.

        Returns:
            max_delta: relative difference between results
            avg_delta: same as max_delta
        """
        max_delta = (self.duration - ref.duration) / ref.duration
        max_delta = max(max_delta, 0)
        avg_delta = max_delta

        return max_delta, avg_delta
