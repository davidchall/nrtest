class Result(object):
    """docstring for Result"""
    def __init__(self, path):
        self.path = path

    def compareBoolean(self, other):
        raise NotImplementedError('abstract method')

    def compareGraded(self, other):
        raise NotImplementedError('abstract method')
