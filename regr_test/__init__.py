from regr_test.__version__ import __version__

import os.path

__all__ = ['run']


class Application(object):
    """The application under test.

    Application metadata is read from a JSON file, e.g.

        import json
        with open('program.json') as f:
            app = Application(**json.load(f))


    Mandatory fields:
        exe: application executable
        setup_script: environment setup script
        version: application version
        tests_path: directory containing tests
        benchmark_path: directory for output files

    Optional fields:
        timeout: time [s] before test is cancelled
        description: string describing version
    """
    def __init__(self, exe, setup_script, version,
                 tests_path, benchmark_path,
                 timeout=None, description=None):
        self.exe = exe
        self.setup_script = setup_script
        self.version = version
        self.tests_path = tests_path
        self.benchmark_path = benchmark_path
        self.timeout = timeout
        self.description = description


class Test(object):
    """A single test.

    Test metadata is read from a JSON file, e.g.

        import json
        with open('test.json') as f:
            test = Test(**json.load(f))


    Mandatory fields:
        args: list of arguments to pass to executable
        version: test version

    Optional fields:
        log_file: file for stdout and stderr
        in_files: list of input files required
        out_files: list of output files generated
        fail_strings: list of strings indicating failure in stdout or stderr
        description: string describing test purpose
    """
    def __init__(self, args, version, log_file=None,
                 in_files=[], out_files=[], fail_strings=[],
                 description=None):
        self.args = args
        self.version = version
        self.log_file = log_file
        self.in_files = in_files
        self.out_files = out_files
        self.fail_strings = fail_strings
        self.description = description

        # Default log filename is constructed from parameter filename
        if not self.log_file:
            param_fname = max(self.args, key=len)  # Assumed to be longest arg
            (basename, _) = os.path.splitext(param_fname)
            self.log_file = basename + '.log'
