from os import makedirs, environ
from os.path import exists, isfile, isdir, join, split
import tempfile
import shutil
import logging
import json

from . import Metadata
from .process import source, execute, monitor
from .utility import color, slugify

PASS = color('passed', 'g')
FAIL = color('failed', 'r')


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
        input_files [list of paths]
        output_files [dict of paths and result types]
        fail_strings: list of strings indicating failure in log file
    """
    _testing_requires = [
        'name',
        'version',
        'args',
    ]
    _testing_allows = {
        'description': None,
        'input_files': [],
        'output_files': {},
        'fail_strings': [],
    }
    _compare_requires = [
        'name',
        'version',
        'description',
        'subdir',
        'out_log',
        'err_log',
        'output_files',
        'passed',
        'error_msg',
    ]

    out_log = 'stdout.log'
    err_log = 'stderr.log'
    perf_log = 'performance.log'

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.subdir = slugify(self.name)

        self.logger = logging.getLogger(self.name)
        if not self.logger.handlers:
            formatter = logging.Formatter('%(name)s: %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.propagate = False

    def execute(self, app, benchmark_path):
        input_dir = self.input_dir
        output_dir = join(benchmark_path, self.subdir)

        try:
            self.logger.debug('Starting execution')
            self._precheck_execute(input_dir, output_dir)
            self._execute(app, input_dir, output_dir)
            self._postcheck_execute(output_dir)
        except TestFailure as e:
            self.passed = False
            self.error_msg = e.value
            self.logger.info(FAIL)
            self.logger.debug(self.error_msg)
        else:
            self.passed = True
            self.error_msg = None
            self.logger.info(PASS)

        return self.passed

    def valid_for_execute(self):
        if not hasattr(self, 'input_dir'):
            logging.error('Test input directory not specified')
            return False

        p = self.input_dir
        if not isdir(p):
            logging.error('Tests directory not found: "%s"' % p)
            return False

        return True

    def valid_for_compare(self):
        return True

    def _precheck_execute(self, input_dir, output_dir):
        for fname in self.input_files:
            fpath = join(input_dir, fname)
            if not isfile(fpath):
                raise TestFailure('Input file not found: "%s"' % fpath)

        if not exists(output_dir):
            makedirs(output_dir)

        for fname in self.output_files.keys() + [self.out_log, self.err_log]:
            fpath = join(output_dir, fname)
            if exists(fpath):
                raise TestFailure('Output file already exists: "%s"' % fpath)

    def _postcheck_execute(self, output_dir):
        # TODO: support regex?
        # TODO: highlight which failure string was found
        if self.fail_strings and len(self.fail_strings) > 0:
            for fname in [self.out_log, self.err_log]:
                fpath = join(output_dir, fname)
                with open(fpath) as f:
                    for line in f:
                        if any(s in line for s in self.fail_strings):
                            raise TestFailure('Failure string found in log')

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
            cmd = ' '.join([app.exe] + self.args)
            env = source(app.setup_script) if app.setup_script else environ

            try:
                with open(join(output_dir, self.out_log), 'w') as f_out:
                    with open(join(output_dir, self.err_log), 'w') as f_err:

                        p = execute(cmd, env=env, cwd=tmpdir,
                                    stdout=f_out, stderr=f_err)

                        (exitcode, perf) = monitor(p, timeout=app.timeout)
                        dur = perf['duration']

            except IOError:
                raise TestFailure('Unable to write log file')

            # Copy output files to benchmark directory
            for fname in self.output_files:
                if isfile(join(tmpdir, fname)):
                    _copy_filepath(fname, tmpdir, output_dir)

        finally:
            shutil.rmtree(tmpdir)

        if exitcode == -11:
            raise TestFailure('Segmentation fault')
        elif exitcode != 0:
            raise TestFailure('Non-zero exit code')

        if dur is None:
            raise TestFailure('Program timed out')

        with open(join(output_dir, self.perf_log), 'w') as f:
            json.dump(perf, f, sort_keys=True, indent=4,
                      separators=(',', ': '))
        self.output_files[self.perf_log] = 'performance'


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
