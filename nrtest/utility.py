# -*- coding: utf-8 -*-

# system imports
import os
import sys
import re
import shutil


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


def copy_file_and_path(rel_path, src_dir, dest):
    """Copy a relative filepath from src_dir to dest, whilst generating any
    directories included in rel_path

    E.g. copy subdir/foo.txt from dir1/ to dir2/ results in dir2/subdir/foo.txt
    """
    folders, _ = os.path.split(rel_path)
    dest = os.path.join(dest, folders)
    if not os.path.isdir(dest):
        os.makedirs(dest)
    shutil.copy(os.path.join(src_dir, rel_path), dest)


def which(program, env):
    """Returns absolute path to first occurence of program in the PATH
    environment variable (echoing the bash script 'which').

    Args:
        program: the executable name or absolute path
        env: the environment to search
    """
    def is_executable(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_executable(program):
            return program
    else:
        for p in env['PATH'].split(os.pathsep):
            p = p.strip('"')
            p = os.path.join(p, program)
            if is_executable(p):
                return p

    return None
