from nrtest import Application
from nrtest.test import Test

from nose.tools import raises

test_execution = {
    'name': 'test',
    'version': 1.0,
    'args': ['config.txt'],
}

test_comparison = {
    'name': 'test',
    'version': 1.0,
    'description': None,
    'log_file': 'out.log',
    'output_files': ['output.txt'],
    'passed': True,
    'error_msg': None,
    'duration': 10.0,
    'performance': None,
}

app_execution = {
    'name': 'app',
    'version': 1.0,
    'exe': 'cat',
    'setup_script': None,
    'tests_path': '/path/to/tests',
    'benchmark_path': '/path/to/benchmarks',
}

app_comparison = {
    'name': 'app',
    'version': 1.0,
    'description': None,
}


def check_required(constructor, data):
    constructor(data)


@raises(ValueError)
def check_unknown_field(constructor, data):
    data['unknown'] = 'value'
    constructor(data)


@raises(ValueError)
def check_missing_field(constructor, data):
    del data['name']
    constructor(data)


def test_generator():
    metadata_types = {
        Test.for_test: test_execution,
        Test.for_compare: test_comparison,
        Application.for_test: app_execution,
        Application.for_compare: app_comparison,
    }

    checks = [
        check_required,
        check_unknown_field,
        check_missing_field,
    ]

    for check in checks:
        for constructor, data in metadata_types.items():
            yield check, constructor, data
