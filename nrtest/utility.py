import sys


def color(string, c):
    if not sys.stdout.isatty():
        return string
    colors = {'r': 31, 'g': 32, 'y': 33, 'b': 34}
    if c not in colors:
        return string
    else:
        return '\033[{0}m{1}\033[0m'.format(colors[c], string)
