# -*- coding: utf-8 -*-

# system imports
import os.path
import logging

# third-party imports
import six

__author__ = 'David Hall'
__version__ = '0.2.1'


class Metadata(dict):
    """Metadata can be accessed using both dictionary and attribute syntax.
    Provides basic validation of input fields, with different requirements for
    the testing and comparison steps.
    """
    execute_required_fields = []
    execute_optional_fields = {}
    compare_required_fields = []

    def __init__(self, *args, **kwargs):
        super(Metadata, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def skim(self):
        return {k: self.get(k, None) for k in self.compare_required_fields}

    @classmethod
    def for_execution(cls, data):
        req, opt = cls.execute_required_fields, cls.execute_optional_fields
        cls._validate(data, req, opt)
        return cls(**data)

    @classmethod
    def for_comparison(cls, data):
        req, opt = cls.compare_required_fields, {}
        cls._validate(data, req, opt)
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
        exe: executable
        setup_script: environment setup script [path]

    Optional fields:
        description
        timeout [float in secs]
    """
    execute_required_fields = [
        'name',
        'version',
        'exe',
    ]
    execute_optional_fields = {
        'description': None,
        'setup_script': None,
        'timeout': None,
    }
    compare_required_fields = [
        'name',
        'version',
        'description',
    ]

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        if hasattr(self, 'setup_script') and self.setup_script is not None:
            self.setup_script = os.path.expanduser(self.setup_script)
            self.setup_script = os.path.abspath(self.setup_script)


class Test(Metadata):
    """When declaring the test in a JSON file...

    Required fields (testing):
        name
        version
        args: arguments to pass to executable [list of strings]

    Optional fields:
        description
        input_files [list of paths]
        output_files [dict of paths and result types]
        fail_strings: list of strings indicating failure in log file
    """
    execute_required_fields = [
        'name',
        'version',
        'args',
    ]
    execute_optional_fields = {
        'description': None,
        'input_files': [],
        'output_files': {},
        'fail_strings': [],
    }
    compare_required_fields = [
        'name',
        'version',
        'description',
        'output_files',
        'passed',
        'error_msg',
    ]

    out_fname = 'stdout.log'
    err_fname = 'stderr.log'
    perf_fname = 'performance.json'

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

        for fname, ftype in six.iteritems(self.output_files):
            if ftype is None:
                self.output_files[fname] = 'null'

        self.logger = logging.getLogger(self.name)
        if not self.logger.handlers:
            formatter = logging.Formatter('%(name)s: %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.propagate = False
