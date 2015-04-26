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
        Test.for_execution: test_execution,
        Test.for_comparison: test_comparison,
        Application.for_execution: app_execution,
        Application.for_comparison: app_comparison,
    }

    checks = [
        check_required,
        check_unknown_field,
        check_missing_field,
    ]

    for check in checks:
        for constructor, data in metadata_types.items():
            yield check, constructor, data.copy()


def test_conversion():
    test = Test.for_execution(test_execution)
    Test.for_comparison(test.skim())
    app = Application.for_execution(app_execution)
    Application.for_comparison(app.skim())
