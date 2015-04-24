from nrtest.test.process import source, execute, monitor

import os
import sys
import tempfile
import shutil
import re


class TestFailure(Exception):
    """Exception raised in case of test failure."""
    def __init__(self, value):
        super(TestFailure, self).__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


def pre_testsuite_checks(app):
    if not os.path.isdir(app.tests_path):
        raise TestFailure('Tests directory not found: "%s"' % app.tests_path)

    if not os.path.isdir(app.benchmark_path):
        os.makedirs(app.benchmark_path)


def pre_test_checks(app, test):
    for fname in test.input_files:
        fpath = os.path.join(app.tests_path, fname)
        if not os.path.isfile(fpath):
            raise TestFailure('Input file not found: "%s"' % fpath)

    for fname in test.output_files + [test.log_file]:
        fpath = os.path.join(app.benchmark_path, fname)
        if os.path.exists(fpath):
            raise TestFailure('Output file already exists: "%s"' % fpath)


def run_test(app, test):
    try:
        tmpdir = tempfile.mkdtemp()
    except OSError:
        raise TestFailure('Unable to open working directory')

    try:
        # Copy input files to working directory
        for fname in test.input_files:
            _copy_filepath(fname, app.tests_path, tmpdir)

        # Test-specific benchmark path
        slug = test.name.strip().replace(' ', '_')
        slug = re.sub(r'(?u)[^-\w.]', '', slug)
        if not os.path.isdir(os.path.join(app.benchmark_path, slug)):
            os.makedirs(os.path.join(app.benchmark_path, slug))

        # Perform test
        test.log_file = os.path.join(slug, test.log_file)
        log_fpath = os.path.join(app.benchmark_path, test.log_file)
        cmd = ' '.join([app.exe] + test.args)
        env = source(app.setup_script)
        try:
            with open(log_fpath, 'w') as log_file:
                p = execute(cmd, env=env, cwd=tmpdir, stdout=log_file)
                (exit_code, dur, perf) = monitor(p, timeout=app.timeout)
        except IOError:
            raise TestFailure('Unable to write log file: "%s"' % test.log_file)

        # Copy output files to benchmark directory

        for fname in test.output_files:
            try:
                dest_dir = os.path.join(app.benchmark_path, slug)
                _copy_filepath(fname, tmpdir, dest_dir)
            except IOError:
                raise TestFailure('Output file not generated: "%s"' % fname)
        test.output_files = [os.path.join(slug, f) for f in test.output_files]
    finally:
        shutil.rmtree(tmpdir)

    if exit_code == -11:
        raise TestFailure('Segmentation fault')
    elif exit_code != 0:
        raise TestFailure('Non-zero exit code')

    if dur is None:
        raise TestFailure('Program timed out (duration > %ss)' % app.timeout)

    return (dur, perf)


def _copy_filepath(path, src_dir, dest):
    """Copy a relative filepath from src_dir to dest, whilst generating any
    directories included in the path.

    E.g. copy subdir/foo.txt from dir1/ to dir2/ results in dir2/subdir/foo.txt
    """
    folders, _ = os.path.split(path)
    dest = os.path.join(dest, folders)
    if not os.path.isdir(dest):
        os.makedirs(dest)
    shutil.copy(os.path.join(src_dir, path), dest)


def post_test_checks(app, test):
    # TODO: support regex?
    # TODO: highlight which failure string was found
    if test.fail_strings and len(test.fail_strings) > 0:
        fpath = os.path.join(app.benchmark_path, test.log_file)
        with open(fpath) as f:
            for line in f:
                if any(s in line for s in test.fail_strings):
                    raise TestFailure('Failure string found in log file')

    for fname in test.output_files:
        fpath = os.path.join(app.benchmark_path, fname)
        if not os.path.isfile(fpath):
            raise TestFailure('Output file not generated: "%s"' % fname)


def execute_testsuite(app, tests):
    # If pre-tests fail, exit before executing any tests
    try:
        pre_testsuite_checks(app)
        for test in tests:
            pre_test_checks(app, test)
    except TestFailure as e:
        print(e.value)
        sys.exit(1)

    for test in tests:
        try:
            (test.duration, test.performance) = run_test(app, test)
            post_test_checks(app, test)
        except TestFailure as e:
            test.passed = False
            test.error_msg = e.value
            test.duration, test.performance = None, None
        except KeyboardInterrupt as e:
            print('Process interrupted by user')
        else:
            test.passed = True
            test.error_msg = None
