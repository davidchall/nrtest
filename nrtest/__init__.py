from nrtest.__version__ import __version__


class Metadata(dict):
    """Metadata can be accessed using both dictionary and attribute syntax.
    Provides basic validation of input fields, with different requirements for
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
