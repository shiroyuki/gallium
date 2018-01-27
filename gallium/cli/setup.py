import codecs
import json
import os
import sys

try:
    import yaml
except ImportError:
    pass

from gallium.interface import ICommand, EmptyResponse


class Init(ICommand):
    def identifier(self):
        return 'init'

    def define(self, parser):
        parser.add_argument('--format', '-f', help = 'Configuration file format, e.g., yaml (or yml), json', default = 'yml', required = False)
        parser.add_argument('--output', '-o', help = 'The path to write the config file (default to the current directory).', required = False)

    def execute(self, args):
        print('>>> This is the setup wizard for a new project.')
        print('>>> NOTE: blank response is to proceed to the next step.\n')

        file_format = (args.format).lower()

        extensions = self._retrieve_list('Extensions (fully-qualified class name, the order matters)')
        commands   = self._retrieve_list('Command to use (only the module/submodule)')

        config_data = {
            'imports'    : commands,
            'extensions' : extensions,
        }

        output_path = os.path.abspath(args.output if args.output else 'cli.{}'.format(file_format))
        output_data = None

        if file_format in ('yaml', 'yml'):
            assert 'yaml' in sys.modules, 'pyyaml is required for this file format'

            output_data = yaml.dump(config_data, default_flow_style = False)
        elif file_format == 'json':
            output_data = json.dumps(config_data, indent = 4, sort_keys = True)
        else:
            self.alert('Unsupported file format')
            self.bail_out()

        print('>>> +------------------------------+')
        print('>>> | Auto-generated Configuration |')
        print('>>> +------------------------------+')
        print(output_data)

        actual_output_path = self.ask('\nWrite to', default = output_path)

        print('>>> Writing to {}'.format(actual_output_path))

        with codecs.open(actual_output_path, 'w') as f:
            f.write(actual_output_path)

        print('>>> Now, you are ready to go.')

    def _retrieve_list(self, message):
        print('{}\n{}'.format(message, '=' * len(message)))

        items = []

        while True:
            try:
                new_item = self.ask(str(len(items) + 1))

                if new_item in items:
                    self.alert('{} already on the list'.format(new_item))

                    continue

                items.append(new_item)
            except EmptyResponse:
                if self.ask('-> Are you done?', ['yes', 'no'], 'yes') == 'yes':
                    print('<- Proceed to the next step')

                    break

        print('')

        return items
