# -*- coding: utf-8 -*-

# system imports
import os
import logging
import tempfile
import shutil
import json
import datetime

# project imports
from .process import source, execute, monitor
from .utility import color, copy_file_and_path, which


class TestFailure(Exception):
    pass


def execute_testsuite(ts):
    success = True
    for test in ts.tests:
        if not execute_test(test, ts.app):
            success = False

    return success


def execute_test(test, app):
    logger = logging.getLogger(test.name)

    if not os.path.exists(test.output_dir):
        os.makedirs(test.output_dir)

    try:
        duration = _execute(test, app)
        _postcheck(test)
    except TestFailure as e:
        test.passed = False
        test.error_msg = str(e)
        logger.info(color('fail', 'r'))
        logger.info(test.error_msg)
    else:
        test.passed = True
        test.error_msg = None
        logger.info(color('pass', 'g'))
        dur_str = str(datetime.timedelta(seconds=duration)).split('.')[0]
        logger.debug('Duration {0}'.format(dur_str))

    return test.passed


def _execute(test, app):
    try:
        tmpdir = tempfile.mkdtemp()
    except OSError:
        raise TestFailure('Unable to open working directory')

    try:
        # Copy input files to working directory
        for fname in test.input_files:
            copy_file_and_path(fname, test.input_dir, tmpdir)

        # Perform test
        cmd = ' '.join([app.exe] + test.args)
        env = source(app.setup_script) if app.setup_script else os.environ

        try:
            p_out = os.path.join(test.output_dir, test.out_fname)
            p_err = os.path.join(test.output_dir, test.err_fname)
            with open(p_out, 'w') as f_out:
                with open(p_err, 'w') as f_err:

                    proc = execute(cmd, env=env, cwd=tmpdir,
                                   stdout=f_out, stderr=f_err)

                    (exitcode, perf) = monitor(proc, timeout=app.timeout)
                    dur = perf['duration']

        except IOError:
            raise TestFailure('Unable to write log file')

        # Copy output files to benchmark directory
        for fname in test.output_files:
            if os.path.isfile(os.path.join(tmpdir, fname)):
                copy_file_and_path(fname, tmpdir, test.output_dir)

    finally:
        shutil.rmtree(tmpdir)

    if exitcode == -11:
        raise TestFailure('Segmentation fault')
    elif exitcode != 0:
        raise TestFailure('Non-zero exit code')

    if dur is None:
        raise TestFailure('Program timed out')

    p_perf = os.path.join(test.output_dir, test.perf_fname)
    with open(p_perf, 'w') as f:
        json.dump(perf, f, sort_keys=True, indent=4, separators=(',', ': '))

    return dur


def _postcheck(test):
    # TODO: support regex?
    # TODO: highlight which failure string was found
    if test.fail_strings and len(test.fail_strings) > 0:
        for fname in [test.out_fname, test.err_fname]:
            p = os.path.join(test.output_dir, fname)
            with open(p) as f:
                for line in f:
                    if any(s in line for s in test.fail_strings):
                        raise TestFailure('Failure string found in log')

    for fname in test.output_files:
        p = os.path.join(test.output_dir, fname)
        if not os.path.isfile(p):
            raise TestFailure('Output file not generated: "%s"' % fname)


def validate_testsuite(ts):
    p = ts.app.setup_script
    if p and not os.path.exists(p):
        logging.error('Unable to find setup script: "%s"' % p)
        return False

    env = source(ts.app.setup_script) if ts.app.setup_script else os.environ
    if not which(ts.app.exe, env):
        logging.error('Unable to find executable: "%s"' % ts.app.exe)
        return False

    for t in ts.tests:
        if not validate_test(t):
            return False

    p = ts.benchmark_path
    if os.path.exists(p):
        logging.error('Benchmark directory already exists: "%s"' % p)
        return False
    else:
        os.makedirs(p)

    return True


def validate_test(test):
    logger = logging.getLogger(test.name)

    # not specified by user, but should be set by now
    additional_required_fields = [
        'input_dir',
        'output_dir',
    ]

    for field in additional_required_fields:
        if not hasattr(test, field):
            logger.error('Unable to find "%s" property' % field)
            return False

    p = test.input_dir
    if not os.path.isdir(p):
        logger.error('Input directory not found: "%s"' % p)
        return False

    for fname in test.input_files:
        p = os.path.join(test.input_dir, fname)
        if not os.path.isfile(p):
            logger.error('Input file not found: "%s"' % p)
            return False

    return True
