from os import makedirs
from os.path import exists, isfile, isdir, join, split, splitext
import tempfile
import re
import shutil
import logging

from nrtest import Metadata
from nrtest.process import source, execute, monitor


class TestFailure(Exception):
    """Exception raised in case of test failure."""
    def __init__(self, value):
        super(TestFailure, self).__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


class Test(Metadata):
    """When declaring the test in a JSON file...

    Required fields (testing):
        name
        version
        args: arguments to pass to executable [list of strings]

    Optional fields:
        description
        log_file [path]
        input_files [list of paths]
        output_files [list of paths]
        fail_strings: list of strings indicating failure in log file
    """
    _testing_requires = [
        'name',
        'version',
        'args',
    ]
    _testing_allows = {
        'description': None,
        'log_file': None,
        'input_files': [],
        'output_files': [],
        'fail_strings': [],
        'timeout': None,
    }
    _compare_requires = [
        'name',
        'version',
        'description',
        'log_file',
        'output_files',
        'passed',
        'error_msg',
        'duration',
        'performance',
    ]

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.slug = _slugify(self.name)

        # Default log filename is constructed from parameter filename
        if not self.log_file:
            param_fname = max(self.args, key=len)  # Assumed to be longest arg
            (basename, _) = splitext(param_fname)
            self.log_file = basename + '.log'

    def execute(self, app):
        input_dir = app.tests_path
        output_dir = join(app.benchmark_path, self.slug)

        try:
            self._precheck_execute(input_dir, output_dir)
            self._execute(app, input_dir, output_dir)
            self._postcheck_execute(output_dir)
        except TestFailure as e:
            self.passed = False
            self.error_msg = e.value
        except KeyboardInterrupt as e:
            print('Process interrupted by user')
        else:
            self.passed = True
            self.error_msg = None

        # Update relative filepath attributes to include slug
        self.log_file = join(self.slug, self.log_file)
        self.output_files = [join(self.slug, f) for f in self.output_files]

    def compare(self):
        raise NotImplementedError

    def _precheck_execute(self, input_dir, output_dir):
        for fname in self.input_files:
            fpath = join(input_dir, fname)
            if not isfile(fpath):
                raise TestFailure('Input file not found: "%s"' % fpath)

        if not exists(output_dir):
            makedirs(output_dir)

        for fname in self.output_files + [self.log_file]:
            fpath = join(output_dir, fname)
            if exists(fpath):
                raise TestFailure('Output file already exists: "%s"' % fpath)

    def _postcheck_execute(self, output_dir):
        # TODO: support regex?
        # TODO: highlight which failure string was found
        if self.fail_strings and len(self.fail_strings) > 0:
            fpath = join(output_dir, self.log_file)
            with open(fpath) as f:
                for line in f:
                    if any(s in line for s in self.fail_strings):
                        raise TestFailure('Failure string found in log file')

        for fname in self.output_files:
            fpath = join(output_dir, fname)
            if not isfile(fpath):
                raise TestFailure('Output file not generated: "%s"' % fname)

    def _execute(self, app, input_dir, output_dir):
        try:
            tmpdir = tempfile.mkdtemp()
        except OSError:
            raise TestFailure('Unable to open working directory')

        try:
            # Copy input files to working directory
            for fname in self.input_files:
                _copy_filepath(fname, input_dir, tmpdir)

            # Perform test
            log_fpath = join(output_dir, self.log_file)
            cmd = ' '.join([app.exe] + self.args)
            env = source(app.setup_script)
            try:
                with open(log_fpath, 'w') as log_file:
                    p = execute(cmd, env=env, cwd=tmpdir, stdout=log_file)
                    (exit_code, dur, perf) = monitor(p, timeout=app.timeout)
            except IOError:
                raise TestFailure('Unable to write log file: "%s"' %
                                  self.log_file)

            # Copy output files to benchmark directory
            for fname in self.output_files:
                if isfile(join(tmpdir, fname)):
                    _copy_filepath(fname, tmpdir, output_dir)

        finally:
            shutil.rmtree(tmpdir)

        if exit_code == -11:
            raise TestFailure('Segmentation fault')
        elif exit_code != 0:
            raise TestFailure('Non-zero exit code')

        if dur is None:
            raise TestFailure('Program timed out')

        self.duration = dur
        self.performance = perf


def _copy_filepath(rel_path, src_dir, dest):
    """Copy a relative filepath from src_dir to dest, whilst generating any
    directories included in the

    E.g. copy subdir/foo.txt from dir1/ to dir2/ results in dir2/subdir/foo.txt
    """
    folders, _ = split(rel_path)
    dest = join(dest, folders)
    if not isdir(dest):
        makedirs(dest)
    shutil.copy(join(src_dir, rel_path), dest)


def _slugify(s):
    slug = s.strip().replace(' ', '_')
    slug = re.sub(r'(?u)[^-\w.]', '', slug)
    return slug
