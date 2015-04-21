from .__version__ import __version__
from . import controller

import os.path
import json


class Metadata(dict):
    """Metadata can be accessed using both dictionary and attribute syntax.
    Provides basic valiation of input fields, with different requirements for
    the testing and comparison steps.
    """
    _compare_requires = []
    _testing_requires = []
    _testing_allows = {}

    def __init__(self, *args, **kwargs):
        super(Metadata, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def skim(self):
        return {k: self.get(k, None) for k in self._compare_requires}

    @classmethod
    def for_test(cls, data):
        requires, allows = cls._testing_requires, cls._testing_allows
        cls._validate(data, requires, allows)
        return cls(**data)

    @classmethod
    def for_compare(cls, data):
        requires, allows = cls._compare_requires, {}
        cls._validate(data, requires, allows)
        return cls(**data)

    @staticmethod
    def _validate(data, required, allowed):
        for k in required:
            if k not in data:
                raise ValueError('Missing field: "%s"' % k)

        for k in data.keys():
            if k not in allowed and k not in required:
                raise ValueError('Unrecognised field: "%s"' % k)

        for k, v in allowed.items():
            if k not in data:
                data[k] = v


class Application(Metadata):
    """When declaring the application in a JSON file...

    Required fields:
        name
        version
        exe: executable [path]
        setup_script: environment setup script [path]
        tests_path [path]
        benchmark_path [path]

    Optional fields:
        description
        timeout [float in secs]
    """
    _testing_requires = [
        'name',
        'version',
        'exe',
        'setup_script',
        'tests_path',
        'benchmark_path',
    ]
    _testing_allows = {
        'description': None,
        'timeout': None,
    }
    _compare_requires = [
        'name',
        'version',
        'description',
    ]

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self['manifest_file'] = 'manifest.json'


class Test(Metadata):
    """When declaring the test in a JSON file...

    Required fields (testing):
        name
        version
        args: arguments to pass to executable [list of strings]

    Optional fields:
        description
        log_file [path]
        input_files [list of paths]
        output_files [list of paths]
        fail_strings: list of strings indicating failure in log file
    """
    _testing_requires = [
        'name',
        'version',
        'args',
    ]
    _testing_allows = {
        'description': None,
        'log_file': None,
        'input_files': [],
        'output_files': [],
        'fail_strings': [],
        'timeout': None,
    }
    _compare_requires = [
        'name',
        'version',
        'description',
        'log_file',
        'output_files',
        'passed',
        'error_msg',
        'duration',
        'performance',
    ]

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

        # Default log filename is constructed from parameter filename
        if not self.log_file:
            param_fname = max(self.args, key=len)  # Assumed to be longest arg
            (basename, _) = os.path.splitext(param_fname)
            self.log_file = basename + '.log'


def write_testsuite_results(app, tests):
    manifest = {
        'Application': app.skim(),
        'Tests': [test.skim() for test in tests]
    }

    manifest_path = os.path.join(app.benchmark_path, app.manifest_file)
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, sort_keys=True, indent=4,
                  separators=(',', ': '))


def read_testsuite_results(manifest_path):
    with open(manifest_path) as f:
        manifest = json.load(f)

    app = Application.for_compare(manifest['Application'])
    tests = [Test.for_compare(test) for test in manifest['Tests']]

    return (app, tests)
