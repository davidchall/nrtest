# system imports
import sys
import re


def color(string, c):
    """Return a colored string, for printing to the terminal.
    """
    colors = {'r': 31, 'g': 32, 'y': 33, 'b': 34}

    if not sys.stdout.isatty() or c not in colors:
        return string
    else:
        return '\033[{0}m{1}\033[0m'.format(colors[c], string)


def slugify(s):
    """Returns a filesystem-friendly version of a string.
    """
    slug = s.strip().replace(' ', '_')
    slug = re.sub(r'(?u)[^-\w.]', '', slug)
    return slug
