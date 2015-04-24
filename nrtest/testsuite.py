import logging
import json
import os.path

from nrtest import Application
from nrtest.test import Test


class TestSuite(object):
    """docstring for TestSuite"""
    def __init__(self, app, tests=[]):
        self.app = app
        self.tests = tests
        self.logger = logging.getLogger()
        self.manifest_fname = 'manifest.json'

    def write_manifest(self):
        """Writes a JSON manifest containing metadata needed for comparison.
        """
        manifest = {
            'Application': self.app.skim(),
            'Tests': [test.skim() for test in self.tests]
        }

        path = os.path.join(self.app.benchmark_path, self.manifest_fname)
        with open(path, 'w') as f:
            json.dump(manifest, f, sort_keys=True, indent=4,
                      separators=(',', ': '))

    @classmethod
    def read_manifest(cls, path):
        """Reads a JSON manifest and returns a TestSuite instance.
        """
        with open(path) as f:
            manifest = json.load(f)

        app = Application.for_compare(manifest['Application'])
        tests = [Test.for_compare(test) for test in manifest['Tests']]

        return cls(app, tests)

    @classmethod
    def read_config(cls, app_fname, test_fnames):
        with open(app_fname) as f:
            app = Application.for_test(json.load(f))

        tests = []
        for fname in test_fnames:
            with open(fname) as f:
                tests.append(Test.for_test(json.load(f)))

        return cls(app, tests)

    def execute(self):
        """Executes tests.
        """
        self._check_execute()
        for test in self.tests:
            test.execute(self.app)

    def compare(self):
        """Compare test results.
        """
        self._check_compare()
        for test in self.tests:
            test.compare()

    def _check_execute(self):
        tests_path = self.app.tests_path
        if not os.path.isdir(tests_path):
            logging.error('Tests directory not found: "%s"' % tests_path)

        bench_path = self.app.benchmark_path
        if os.path.exists(bench_path):
            logging.error('Benchmark directory already exists: "%s"' %
                          bench_path)
        else:
            os.makedirs(bench_path)

    def _check_compare(self):
        pass
