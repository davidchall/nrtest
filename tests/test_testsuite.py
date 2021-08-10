#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_testsuite
----------------------------------

Tests for validation of TestSuite.
"""

import os.path
import tempfile
import unittest

from nrtest import Application, Test
from nrtest.execute import validate_testsuite
from nrtest.testsuite import TestSuite
from nrtest.utility import rmtree

app1 = Application.for_execution({
    'name': 'app',
    'version': '1.3.0',
    'exe': 'echo',
})

app2 = Application.for_execution({
    'name': 'app',
    'version': '1.2.0',
    'exe': 'echo',
})

test1 = Test.for_execution({
    'name': 'cat',
    'version': '1.0',
    'args': ['cat'],
})

test2 = Test.for_execution({
    'name': 'cat',
    'version': '1.0',
    'args': ['dog'],
    'minimum_app_version': '1.3.0',
})


class TestMinimumAppVersion(unittest.TestCase):
    def setUp(self):
        self.benchmark_path = os.path.join(tempfile.gettempdir(), "benchmark")

    def tearDown(self):
        rmtree(self.benchmark_path)

    def test_sufficient_app_version(self):
        ts = TestSuite(app1, [test1, test2], self.benchmark_path)
        self.assertTrue(validate_testsuite(ts))
        self.assertEqual(len(ts.tests), 2)

    def test_insufficient_app_version(self):
        ts = TestSuite(app2, [test1, test2], self.benchmark_path)
        self.assertTrue(validate_testsuite(ts))
        self.assertEqual(len(ts.tests), 1)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
