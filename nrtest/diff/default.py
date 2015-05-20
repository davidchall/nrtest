import filecmp

from .factory import register, BaseDiff


@register('default', 'eps')
class DefaultDiff(BaseDiff):
    """A default comparison of result files, which is similar to the command
    line utility `diff`.
    """
    def __init__(self, *args, **kwargs):
        super(DefaultDiff, self).__init__(*args, **kwargs)

        self.diff = filecmp.cmp(self.path_t, self.path_r, shallow=False)

    def max(self):
        return 0 if self.diff else 999.9

    def min(self):
        return self.max()

    def mean(self):
        return self.max()
