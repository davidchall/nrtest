# system imports
import logging


def execute_testsuite(ts):
    """Execute the testsuite.

    Returns: boolean success
    """
    if not ts.valid_for_execute():
        return False

    success = True
    for test in sorted(ts.tests):
        if not execute_test(test, ts.app, ts.benchmark_path):
            success = False

    return success


def execute_test(test, app, benchmark_path):
    return test.execute(app, benchmark_path)
