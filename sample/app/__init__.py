from gallium.interface import ICommand

class Default(ICommand):
    def identifier(self):
        return 'sample.default'

    def define(self, parser):
        pass

    def execute(self, args):
        print(self.__class__.__name__)
