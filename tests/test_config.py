#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
----------------------------------

Tests for input validation of tests and apps.
"""

import unittest

from nrtest import Application, Test

test_execution = {
    'name': 'test',
    'version': 1.0,
    'args': ['config.txt'],
}

test_comparison = {
    'name': 'test',
    'version': 1.0,
    'description': None,
    'output_files': {'output.txt': 'default'},
    'passed': True,
    'error_msg': None,
}

app_execution = {
    'name': 'app',
    'version': 1.0,
    'exe': 'cat',
}

app_comparison = {
    'name': 'app',
    'version': 1.0,
    'description': None,
}


class TestExecuteTest(unittest.TestCase):
    def setUp(self):
        self.constructor = Test.for_execution
        self.data = test_execution.copy()

    def test_required(self):
        self.constructor(self.data)

    def test_unknown_field(self):
        self.data['unknown'] = 'value'
        with self.assertRaises(ValueError):
            self.constructor(self.data)

    def test_missing_field(self):
        del self.data['name']
        with self.assertRaises(ValueError):
            self.constructor(self.data)


class TestCompareTest(TestExecuteTest):
    def setUp(self):
        self.constructor = Test.for_comparison
        self.data = test_comparison.copy()


class TestExecuteApp(TestExecuteTest):
    def setUp(self):
        self.constructor = Application.for_execution
        self.data = app_execution.copy()


class TestCompareApp(TestExecuteTest):
    def setUp(self):
        self.constructor = Application.for_comparison
        self.data = app_comparison.copy()


class TestConversion(unittest.TestCase):
    def test_convert_test(self):
        test = Test.for_execution(test_execution)
        Test.for_comparison(test.skim())

    def test_convert_app(self):
        app = Application.for_execution(app_execution)
        Application.for_comparison(app.skim())


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
