# -*- coding: utf-8 -*-

# system imports
import os
import logging

# third-party imports
import six

# project imports
from .utility import color
from .plugin import find_unique_function


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
    if tests_sut.keys() != tests_ref.keys():
        logging.warning('SUT and benchmark contain different tests')

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
        for fname, ftype in six.iteritems(test_sut.output_files):

            ftype = ftype.lower()
            path_sut = os.path.join(test_sut.output_dir, fname)
            path_ref = os.path.join(test_ref.output_dir, fname)

            if not os.path.exists(path_sut):
                raise CompareException('Output file not found: %s' % path_sut)
            if not os.path.exists(path_ref):
                raise CompareException('Output file not found: %s' % path_ref)

            compare_file = find_unique_function('compare', ftype)
            try:
                compatible = compare_file(path_sut, path_ref, rtol, atol)
            except Exception as e:
                logger.debug(str(e))
                raise CompareException('Unexpected error occurred during diff')

            if not compatible:
                raise CompareException('%s: diff failed' % fname)

    except CompareException as e:
        logger.info(color('fail', 'r'))
        logger.info(str(e))
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

    file_types = set(ft for t in ts.tests for ft in t.output_files.values())
    for ft in file_types:
        if find_unique_function('compare', ft) is None:
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


##################################
# Bundled compare_file functions #
##################################
def default_compare(path_test, path_ref, rtol, atol):
    """A default comaprison, which is similar to the diff utility.
    """
    import filecmp
    return filecmp.cmp(path_test, path_ref, shallow=False)


def null_compare(path_test, path_ref, rtol, atol):
    """A null comparison. This is used when a result file is required to be
    produced by a test, but it is not possible to compare to a benchmark.
    """
    return True
