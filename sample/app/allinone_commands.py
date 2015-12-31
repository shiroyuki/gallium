import os

from gallium.interface import ICommand

class Dummy(ICommand):
    def identifier(self):
        return 'sample.dummy'

    def execute(self, args):
        print(self.__class__.__name__)

class FileLister(ICommand):
    def identifier(self):
        return 'sample.file_lister'

    def define(self, parser):
        parser.add_argument(
            'path',
            help='the path to list'
        )

    def execute(self, args):
        current_directory = os.getcwd()

        target_directory = args.path or current_directory

        for name in os.listdir(target_directory):
            print(name)
