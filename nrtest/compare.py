# system imports
import logging
from os.path import join

# nrtest imports
from .diff import factory, DiffException
from .utility import color


class CompareException(Exception):
    pass


def compare_testsuite(ts_sut, ts_ref, tolerance):
    """Compare testsuite results against a benchmark.

    Args:
        ts_sut: SUT testsuite
        ts_ref: benchamrk testsuite
        tolerance: relative precision at which results considered compatible

    Returns:
        Boolean: whether results are compatible
    """
    # check each testsuite is individually valid before beginning
    try:
        ts_sut.validate_for_compare()
        ts_ref.validate_for_compare()
    except Exception as e:
        logging.error(str(e))
        return False

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

        test_sut.dir = join(ts_sut.dir, test_sut.dir)
        test_ref.dir = join(ts_ref.dir, test_ref.dir)

        if not compare_test(test_sut, test_ref, tolerance):
            compatible = False

    return compatible


def compare_test(test_sut, test_ref, tolerance):
    """Compare test results against a benchmark.

    Args:
        test_sut: SUT test
        test_ref: benchmark test
        tolerance: relative precision at which results considered compatible

    Returns:
        Boolean: whether results are compatible
    """
    logger = logging.getLogger(test_sut.name)

    compatible = True
    try:
        # check tests are comparable
        if test_sut.name != test_ref.name:
            msg = 'Attempted to compare to %s' % test_ref.name
            raise CompareException(msg)

        if test_sut.output_files != test_ref.output_files:
            raise CompareException('Benchmark has different output files')

        # compare result files
        # return False immediately if any are incompatible
        max_diff = 0.0
        for fname, ftype in test_sut.output_files.iteritems():
            path_sut = join(test_sut.dir, fname)
            path_ref = join(test_ref.dir, fname)

            try:
                diff = factory(ftype)(path_sut, path_ref)
            except DiffException as e:
                raise CompareException(str(e))

            if diff is None:
                continue
            if not diff.numeric:
                if diff.fail():
                    raise CompareException('Incompatible file: "%s"' % fname)
            else:
                max_diff = max(max_diff, diff.max())

    except CompareException as e:
        logger.debug('%s: %s' % (test_sut.name, str(e)))
        logger.info(color('fail', 'r'))
        compatible = False

    else:
        grade = '{:.2%}'.format(max_diff)
        if max_diff > tolerance:
            logger.info(color(grade, 'r'))
            compatible = False
        else:
            logger.info(color(grade, 'g'))

    return compatible
