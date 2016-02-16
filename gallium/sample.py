import pprint
from gallium.interface import ICommand

class ArgsInspector(ICommand):
    def identifier(self):
        return 'args.inspect'

    def define(self, parser):
        parser.add_argument(
            '--debug',
            '-d',
            action = 'store_true'
        )

    def execute(self, args):
        pp = pprint.PrettyPrinter(indent=2)

        arguments = {
            name: getattr(args, name)
            for name in dir(args)
            if name[0] != '_' and not callable(getattr(args, name))
        }

        pp.pprint(arguments)