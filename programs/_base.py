class BaseTest:
    def __init__(self, *args, **kwargs):
        self.filename = kwargs['filename']

    def execute(self):
        pass

    def print_results(self):
        pass
