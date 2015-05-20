from .factory import register, NumericDiff


@register('duration')
class DurationDiff(NumericDiff):
    """Compare to a reference result. The comparison is one-sided because only
    an increase in duration is considered a failure.
    """
    def __init__(self, dur_test, dur_ref):
        # we do not use base constructor, which assumes diff inputs are files
        self.dur_t = dur_test
        self.dur_r = dur_ref
        self.diff = (self.dur_t - self.dur_r) / self.dur_r
        self.diff = max(self.diff, 0)

    def max(self):
        return self.diff

    def min(self):
        return self.max()

    def mean(self):
        return self.max()
