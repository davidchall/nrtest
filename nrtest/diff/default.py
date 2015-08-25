# system imports
import filecmp

# project imports
from .factory import register, BooleanDiff


@register('default', 'eps')
class DefaultDiff(BooleanDiff):
    """A default comparison of result files, which is similar to the command
    line utility `diff`.
    """
    def __init__(self, *args, **kwargs):
        super(DefaultDiff, self).__init__(*args, **kwargs)

        self.diff = not filecmp.cmp(self.path_t, self.path_r, shallow=False)

    def fail(self):
        return self.diff


@register(None, 'none', 'null')
class NoneDiff(BooleanDiff):
    """A dummy class used to neglect the comparison of results files."""
    def __init__(self, *args, **kwargs):
        super(NoneDiff, self).__init__(*args, **kwargs)

    def fail(self):
        return False
