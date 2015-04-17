from regr_test.__version__ import __version__

import os.path
import json


class Metadata(dict):
    """Metadata can be accessed using both dictionary and attribute syntax.
    Provides basic valiation of input fields, with different requirements for
    the testing and reading (needed for comparison) steps.
    """
    _read_requires = []
    _test_requires = []
    _allowed = []

    def __init__(self, *args, **kwargs):
        super(Metadata, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for k in self._allowed:
            if k not in self:
                self[k] = None

    @classmethod
    def for_testing(cls, data):
        cls._validate(data, cls._test_requires, cls._allowed)
        return cls(**data)

    @classmethod
    def for_reading(cls, data):
        cls._validate(data, cls._read_requires, cls._allowed)
        return cls(**data)

    @classmethod
    def from_json(cls, path):
        with open(path) as f:
            data = json.load(f)
        return cls.for_testing(data)

    @classmethod
    def from_sqlite(cls, row):
        data = {k: row[k] for k in row.keys()}
        return cls.for_reading(data)

    @staticmethod
    def _validate(data, required, allowed):
        for k in required:
            if k not in data:
                raise ValueError('Missing field: "%s"' % k)

        for k in data.keys():
            if k not in allowed:
                raise ValueError('Unrecognised field: "%s"' % k)


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

    _read_requires = ['name', 'version']
    _test_requires = ['exe', 'setup_script', 'tests_path', 'benchmark_path']
    _test_requires += _read_requires
    _allowed = ['description', 'timeout'] + _test_requires


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

    _read_requires = ['name', 'version', 'passed']
    _test_requires = ['name', 'version', 'args']
    _allowed = ['log_file', 'input_files', 'output_files', 'fail_strings',
                'passed', 'error_msg', 'duration', 'performance',
                'description'] + _test_requires

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

        # Default log filename is constructed from parameter filename
        if not self.log_file:
            param_fname = max(self.args, key=len)  # Assumed to be longest arg
            (basename, _) = os.path.splitext(param_fname)
            self.log_file = basename + '.log'

    @classmethod
    def for_testing(cls, data):
        obj = super(Test, cls).for_testing(data)

        # These are results of test, so don't read from file
        obj.passed = False
        obj.error_msg = None
        obj.duration = None
        obj.performance = None

        return obj
