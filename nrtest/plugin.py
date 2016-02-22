# -*- coding: utf-8 -*-

# system imports
import logging
from pkg_resources import iter_entry_points


def find_unique_function(action, filetype):
    group = 'nrtest.' + action
    entry_points = list(iter_entry_points(group, filetype))

    if len(entry_points) == 0:
        msg = ('Cannot locate a {0} function for the "{1}" filetype. '
               'Please consult the documentation if you are attempting to '
               'use your own extension').format(action, filetype)
        logging.error(msg)
        return None

    elif len(entry_points) > 1:
        msg = ('Discovered multiple {0} functions for the "{1}" filetype. '
               'They were discovered in the packages: {2}'
               ).format(action, filetype, [ep.dist for ep in entry_points])
        logging.error(msg)
        return None

    else:
        return entry_points[0].load()
