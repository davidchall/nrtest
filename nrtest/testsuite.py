# system imports
import logging
import json
import os.path

# nrtest imports
from nrtest import Application
from nrtest.test import Test


class TestSuite(object):
    """The TestSuite class stores metadata about the application under test
    and the tests themselves. It also provides the interface to benchmarks.
    """
    manifest_fname = 'manifest.json'

    def __init__(self, app, tests, benchmark_path):
        """Constructs an instance of the TestSuite class.

        Args:
            app: Application object
            tests: list of Test objects
            benchmark_path: path to the benchmark directory
        """
        self.app = app
        self.tests = tests
        self.benchmark_path = benchmark_path

    @classmethod
    def read_config(cls, app_config_path, test_config_paths, benchmark_path):
        """Constructs a TestSuite instance from a set of JSON config files,
        which is suitable for execute commands.

        Args:
            app_config_path: path to application config file
            test_config_paths: list of paths to test config files
            benchmark_path: path to output directory
        """
        with open(app_config_path) as f:
            app = Application.for_execution(json.load(f))

        tests = []
        for p in test_config_paths:
            with open(p) as f:
                test = Test.for_execution(json.load(f))
                test.input_dir = os.path.dirname(p)
                tests.append(test)

        return cls(app, tests, benchmark_path)

    @classmethod
    def read_benchmark(cls, benchmark_path):
        """Constructs a TestSuite instance from a benchmark directory,
        which is suitable for compare commands.

        This reads metadata from a JSON manifest, and constructs the
        Application instance and each of the Test instances.
        """
        manifest_path = os.path.join(benchmark_path, cls.manifest_fname)
        with open(manifest_path) as f:
            manifest = json.load(f)

        app = Application.for_comparison(manifest['Application'])
        tests = [Test.for_comparison(test) for test in manifest['Tests']]

        return cls(app, tests, benchmark_path)

    def write_manifest(self):
        """Writes a JSON manifest containing application and test metadata
        needed for compare commands.

        Output format must remain compatible with the read_benchmark() method.
        """
        manifest = {
            'Application': self.app.skim(),
            'Tests': [test.skim() for test in self.tests]
        }

        path = os.path.join(self.benchmark_path, self.manifest_fname)
        with open(path, 'w') as f:
            json.dump(manifest, f, sort_keys=True, indent=4,
                      separators=(',', ': '))

    def valid_for_execute(self):
        """Validates the presence of files and directories needed for execute
        commands.

        If this returns false, the nrtest script shall exit before executing
        any tests.
        """
        p = self.benchmark_path
        if os.path.exists(p):
            logging.error('Benchmark directory already exists: "%s"' % p)
            return False
        else:
            os.makedirs(p)

        for test in self.tests:
            if not test.valid_for_execute():
                return False

        return True

    def valid_for_compare(self):
        """Validates the presence of files and directories needed for compare
        commands.

        If this returns false, the nrtest script shall exit before comparing
        any tests.
        """
        p = self.benchmark_path
        if not os.path.isdir(p):
            logging.error('Benchmark directory not found: "%s"' % p)
            return False

        for test in self.tests:
            if not test.valid_for_compare():
                return False

        return True
