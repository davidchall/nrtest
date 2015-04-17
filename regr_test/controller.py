from regr_test import run

import os
import tempfile
import shutil


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
        raise TestFailure('Benchmark directory not found: "%s"' %
                          app.benchmark_path)


def pre_test_checks(app, test):
    for fname in test.in_files:
        fpath = os.path.join(app.tests_path, fname)
        if not os.path.isfile(fpath):
            raise TestFailure('Input file not found: "%s"' % fpath)

    for fname in test.out_files + [test.log_file]:
        fpath = os.path.join(app.benchmark_path, fname)
        if os.path.exists(fpath):
            raise TestFailure('Output file already exists: "%s"' % fpath)


def perform_test(app, test):
    try:
        tmpdir = tempfile.mkdtemp()
    except OSError:
        raise TestFailure('Unable to open working directory')

    try:
        # Copy input files to working directory
        for fname in test.in_files:
            folder, _ = os.path.split(fname)
            dest_dir = os.path.join(tmpdir, folder)
            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(os.path.join(app.tests_path, fname), dest_dir)

        # Perform test
        log_fpath = os.path.join(app.benchmark_path, test.log_file)
        cmd = ' '.join([app.exe] + test.args)
        env = run.source(app.setup_script)

        with open(log_fpath, 'w') as log_file:
            p = run.execute(cmd, env=env, cwd=tmpdir, stdout=log_file)
            (exit_code, duration, perf) = run.monitor(p, timeout=app.timeout)

        # Copy output files to benchmark directory
        for fname in test.out_files:
            folder, _ = os.path.split(fname)
            dest_dir = os.path.join(app.benchmark_path, folder)
            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(os.path.join(tmpdir, fname), dest_dir)

    except IOError:
        raise TestFailure('Unable to write log file: "%s"' % test.log_file)
    finally:
        shutil.rmtree(tmpdir)

    if exit_code == -11:
        raise TestFailure('Segmentation fault')
    elif exit_code != 0:
        raise TestFailure('Non-zero exit code')

    if duration is None:
        raise TestFailure('Program timed out (duration > %ss)' % app.timeout)

    return (duration, perf)


def post_test_checks(app, test):
    # TODO: support regex?
    # TODO: highlight which failure string was found
    if len(test.fail_strings) > 0:
        fpath = os.path.join(app.benchmark_path, test.log_file)
        with open(fpath) as f:
            for line in f:
                if any(s in line for s in test.fail_strings):
                    raise TestFailure('Failure string found in log file')

    for fname in test.out_files:
        fpath = os.path.join(app.benchmark_path, fname)
        if not os.path.isfile(fpath):
            raise TestFailure('Output file not generated: "%s"' % fname)
