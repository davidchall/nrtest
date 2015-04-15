from regr_test.__version__ import __version__

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

    Optional fields:
        description: string describing version
    """
    def __init__(self, exe, setup_script, version, description=None):
        self.exe = exe
        self.setup_script = setup_script
        self.version = version
        self.description = description


class Test(object):
    """A single test.

    Test metadata is read from a JSON file, e.g.

        import json
        with open('test.json') as f:
            test = Test(**json.load(f))


    Mandatory fields:
        args: list of arguments to pass to executable
        cwd: working directory used in test
        version: test version

    Optional fields:
        log_file: file for stdout and stderr
        input_files: list of input files required
        output_files: list of output files generated
        description: string describing test purpose
    """
    def __init__(self, args, cwd, version, log_file=None,
                 input_files=[], output_files=[], description=None):
        self.args = args
        self.cwd = cwd
        self.version = version
        self.log_file = log_file
        self.input_files = input_files
        self.output_files = output_files
        self.description = description

        # Default log filename is constructed from parameter filename
        if not self.log_file:
            import os
            param_fname = max(self.args, key=len)  # Assumed to be longest arg
            (basename, _) = os.path.splitext(param_fname)
            self.log_file = basename + '.log'
