""" Prototype for Tori 4.0+ and Imagination 1.10+

    :Author: Juti Noppornpitak
"""

import argparse
import json
import os
import sys

from imagination.loader import Loader

from .core       import Core
from .ext.helper import activate
from .helper     import Reflector
from .interface  import ICommand, IExtension, alias_property_name

class AliasNotRegisteredError(RuntimeError): pass

class Console(object):
    """ Console

        This is designed to handle subcommands and extensions.
    """
    CONST_CONF_KEY_CMD_SETTINGS = 'settings'

    def __init__(self, name, core = None, config={}, config_path=None, loaders=[]):
        self.name   = name
        self.core   = core or Core()
        self.config = config

        if config_path:
            with open(config_path) as f:
                self.config.update(json.load(f))

        activate(self.core, self.config)

        self.loaders  = loaders
        self.commands = {}
        self.aliases  = {}
        self.settings = {}

    def activate(self):
        main_parser = argparse.ArgumentParser(self.name)
        subparsers  = main_parser.add_subparsers(
            description = 'Available subcommands discovered by the configuration'
        )

        self._define_primary(main_parser)

        try:
            self.settings.update(self.config[type(self).CONST_CONF_KEY_CMD_SETTINGS])
        except KeyError as e:
            pass # not settings overridden

        loading_targets = []

        for loader in self.loaders:
            key = loader.configuration_section_name()

            try:
                loader_config = self.config[key]
            except KeyError as e:
                continue # nothing to load with this loader

            loading_targets.extend([
                (identifier, kind, command)
                for identifier, kind, command in loader.all(loader_config)
            ])

        loading_targets.sort(key=lambda target: target[0]) # sort by identifier

        # Register commands.
        for identifier, kind, command in loading_targets:
            self._register_command(subparsers, identifier, kind, command)

        # If commands do not exist...
        if not self.commands:
            print('No commands available')

            sys.exit(15)

        # Parse arguments and execute.
        args, unknown_args = main_parser.parse_known_args()

        if not hasattr(args, 'func') or unknown_args:
            if len(sys.argv) > 1 and sys.argv[1] in self.commands:
                self.commands[sys.argv[1]]['parser'].print_help()
            else:
                main_parser.print_help()

            sys.exit(15)

        try:
            args.func(args)
        except KeyboardInterrupt as e:
            sys.exit(15)

    def _define_primary(self, main_parser):
        main_parser.add_argument(
            '--process-debug',
            help   = self._reencode_doc('Process-wide debug flag (this may or may not run Gallium in the debug mode.)'),
            action = 'store_true'
        )

    def _register_command(self, subparsers, identifier, cls, command_instance):
        # Handle the command interface.
        self._add_parser(
            subparsers,
            identifier,
            (
                Reflector.short_description(cls) \
                or '(See {}.{})'.format(cls.__module__, cls.__name__)
            ),
            command_instance
        )

        # Handle aliasing.
        if hasattr(command_instance, alias_property_name):
            for alias in getattr(command_instance, alias_property_name):
                self.aliases[alias] = identifier

                self._add_parser(
                    subparsers,
                    alias,
                    '\u2192 Alias to "{}"'.format(identifier),
                    command_instance
                )

    def _add_parser(self, subparsers, identifier, documentation, command_instance):
        if identifier in self.commands:
            registered_command_instance = self.commands[identifier]['instance']
            registered_command_class    = type(registered_command_instance)
            registered_command_fqcn     = Reflector.fqcn(registered_command_class)
            registered_command_doc      = Reflector.short_description(registered_command_class)
            target_command_fqcn         = Reflector.fqcn(type(command_instance))

            raise AliasNotRegisteredError(
                'Cannot set "{}" for {} as it refers to {} ({})'.format(
                    identifier,
                    target_command_fqcn,
                    registered_command_fqcn,
                    registered_command_doc
                )
            )

        parser = subparsers.add_parser(identifier, help = self._reencode_doc(documentation))
        parser.set_defaults(func=command_instance.execute)

        command_instance.define(parser)
        command_instance.set_core(self.core)
        command_instance.set_settings(self.settings)

        self.commands[identifier] = {
            'parser':   parser,
            'instance': command_instance,
        }

    def _reencode_doc(self, text):
        # For non-Windows OSes, this is unnecessary.
        if os.name != 'nt':
            return text

        return text.encode('ascii', 'ignore').decode('ascii', 'ignore')
