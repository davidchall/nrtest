# system imports
import logging

# project imports
from . import Metadata


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

        self.logger = logging.getLogger(self.name)
        if not self.logger.handlers:
            formatter = logging.Formatter('%(name)s: %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.propagate = False
