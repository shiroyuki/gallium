""" Prototype for Tori 4.0+ and Imagination 1.10+

    :Author: Juti Noppornpitak
"""

import argparse
import json
import sys

from imagination.loader import Loader

from .core      import Core
from .interface import ICommand, IExtension

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

        extension_fqcns = config['extensions'] \
            if 'extensions' in config \
            else []

        # Default extensions.
        if 'gallium.ext.imagination.Extension' not in extension_fqcns:
            extension_fqcns.insert(0, 'gallium.ext.imagination.Extension')

        if extension_fqcns:
            for extension_fqcn in extension_fqcns:
                extension_class = Loader(extension_fqcn).package

                if not issubclass(extension_class, IExtension):
                    raise ValueError('{} is not a subclass of {}.'.format(
                        extension_class.__name__,
                        IExtension.__name__
                    ))

                extension = extension_class()

                config_key = extension.config_key()
                ext_config = config[config_key] if config_key and config_key in config else None

                if config_key is None:
                    # NOTE the extension will run without
                    extension.initialize(self.core)
                elif config_key and ext_config:
                    extension.initialize(self.core, ext_config)

        self.loaders = loaders

    def activate(self):
        main_parser = argparse.ArgumentParser(self.name)
        subparsers  = main_parser.add_subparsers(help='sub-commands')

        self._define_primary(main_parser)

        commands = {}

        for loader in self.loaders:
            key      = loader.configuration_section_name()
            settings = self.config[self.CONST_CONF_KEY_CMD_SETTINGS] \
                if self.CONST_CONF_KEY_CMD_SETTINGS in self.config \
                else {}

            if key in self.config and self.config[key]:
                for identifier, kind, command in loader.all(self.config[key]):
                    self._register_command(subparsers, identifier, kind, command)

                    command.set_core(self.core)
                    command.set_settings(settings)

                    commands[identifier] = command

        if not commands:
            print('No commands available')

            sys.exit(15)

        args = main_parser.parse_args()

        if not hasattr(args, 'func'):
            main_parser.print_help()

            sys.exit(15)

        try:
            args.func(args)
        except KeyboardInterrupt as e:
            sys.exit(15)

    def _define_primary(self, main_parser):
        main_parser.add_argument(
            '--debug-global',
            help   = 'Enable the global debug mode',
            action = 'store_true'
        )

    def _register_command(self, subparsers, identifier, cls, instance):
        documentation  = cls.__doc__
        command_parser = subparsers.add_parser(identifier, help=documentation)

        instance.define(command_parser)
        command_parser.set_defaults(func=instance.execute)

    def _prepare_db_connections(self):
        self.core.prepare_db_connections(self.config['db'])
