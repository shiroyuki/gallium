from carbon.interface import ICommand

class Dummy(ICommand):
    def identifier(self):
        return 'sample.dummy'

    def execute(self, args):
        print(self.__class__.__name__)

class FileLister(ICommand):
    def identifier(self):
        return 'sample.file_lister'

    def define(self, parser):
        pass

    def execute(self, args):
        print(self.__class__.__name__)
