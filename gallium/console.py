""" Prototype for Tori 4.0+ and Imagination 1.10+

    :Author: Juti Noppornpitak
"""

import argparse
import json
import sys

from .interface import ICommand

class Console(object):
    CONST_CONF_KEY_CMD_SETTINGS = 'settings'

    def __init__(self, name, core, config_path=None, loaders=[]):
        self.name   = name
        self.core   = core
        self.config = {}

        if config_path:
            with open(config_path) as f:
                self.config.update(json.load(f))

            if 'db' in self.config:
                self._prepare_db_connections()

        self.loaders = loaders

    def activate(self):
        main_parser = argparse.ArgumentParser(self.name)
        subparsers  = main_parser.add_subparsers(help='sub-commands')

        commands = {}

        for loader in self.loaders:
            key = loader.configuration_section_name()

            if key in self.config and self.config[key]:
                for identifier, kind, command in loader.all(self.config[key]):
                    self._register_command(subparsers, identifier, kind, command)

                    command.set_core(self.core)
                    command.set_settings(
                        self.config[self.CONST_CONF_KEY_CMD_SETTINGS]
                        if self.CONST_CONF_KEY_CMD_SETTINGS in self.config
                        else {}
                    )

                    commands[identifier] = command

        if not commands:
            print('No commands available')

            sys.exit(15)

        args = main_parser.parse_args()

        try:
            args.func(args)
        except KeyboardInterrupt as e:
            sys.exit(15)

    def _register_command(self, subparsers, identifier, cls, instance):
        documentation  = cls.__doc__
        command_parser = subparsers.add_parser(identifier, help=documentation)

        instance.define(command_parser)
        command_parser.set_defaults(func=instance.execute)

    def _prepare_db_connections(self):
        self.core.prepare_db_connections(self.config['db'])
