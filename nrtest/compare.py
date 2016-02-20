# -*- coding: utf-8 -*-

# system imports
import os
import logging

# project imports
from .result import create
from .utility import color


class CompareException(Exception):
    pass


def compare_testsuite(ts_sut, ts_ref, rtol, atol):
    """Compare the results of a testsuite against a benchmark.

    Args:
        ts_sut: SUT testsuite
        ts_ref: benchmark testsuite
        tolerance: relative precision at which results considered compatible

    Returns: boolean compatibility
    """
    # check testsuites are comparable
    tests_sut = {t.name: t for t in ts_sut.tests}
    tests_ref = {t.name: t for t in ts_ref.tests}
    if not set(tests_sut.keys()).issubset(tests_ref.keys()):
        logging.error('SUT and benchmark contain different tests')
        return False

    # compare all tests and return False if any are incompatible
    compatible = True
    for name in sorted(tests_sut):
        test_sut = tests_sut[name]
        test_ref = tests_ref[name]

        if not compare_test(test_sut, test_ref, rtol, atol):
            compatible = False

    return compatible


def compare_test(test_sut, test_ref, rtol, atol):
    """Compare the results of a single test against a benchmark.

    Args:
        test_sut: SUT test
        test_ref: benchmark test
        tolerance: relative precision at which results considered compatible

    Returns: boolean compatibility
    """
    logger = logging.getLogger(test_sut.name)

    compatible = True
    try:
        # check tests are comparable
        if test_sut.name != test_ref.name:
            msg = 'Attempted to compare to %s' % test_ref.name
            raise CompareException(msg)

        if test_sut.output_files.keys() != test_ref.output_files.keys():
            raise CompareException('Benchmark has different output files')

        # compare result files
        # return False immediately if any are incompatible
        for fname, ftype in test_sut.output_files.iteritems():
            path_sut = os.path.join(test_sut.output_dir, fname)
            path_ref = os.path.join(test_ref.output_dir, fname)

            if not os.path.exists(path_sut):
                raise CompareException('Output file not found: %s' % path_sut)
            if not os.path.exists(path_ref):
                raise CompareException('Output file not found: %s' % path_ref)

            result_sut = create(ftype)(path_sut)
            result_ref = create(ftype)(path_ref)

            compatible = result_sut.compatible(result_ref, rtol, atol)

            if not compatible:
                raise CompareException('%s: diff failed' % fname)

    except CompareException as e:
        logger.info(color('fail', 'r'))
        logger.debug(str(e))
        compatible = False

    else:
        logger.info(color('pass', 'g'))

    return compatible


def validate_testsuite(ts):
    """Validates the presence of files and directories needed for compare
    commands.
    """
    p = ts.benchmark_path
    if not os.path.isdir(p):
        logging.error('Benchmark directory not found: "%s"' % p)
        return False

    p = os.path.join(ts.benchmark_path, ts.manifest_fname)
    if not os.path.exists(p):
        logging.error('Benchmark manifest not found: "%s"' % p)
        return False

    for t in ts.tests:
        if not validate_test(t):
            return False

    return True


def validate_test(test):
    logger = logging.getLogger(test.name)

    # not specified by user, but should be set by now
    additional_required_fields = [
        'output_dir',
    ]

    for field in additional_required_fields:
        if not hasattr(test, field):
            logger.error('Unable to find "%s" property' % field)
            return False

    return True
