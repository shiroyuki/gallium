""" Prototype for Tori 4.0+ and Imagination 1.10+

    :Author: Juti Noppornpitak
"""

import argparse
from contextlib import contextmanager
import importlib
import json
import re
import types

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer
from imagination.entity  import CallbackProxy
from imagination.entity  import Entity
from imagination.loader  import Loader
from imagination.locator import Locator

from tori.common import get_logger

from .core import Core
from .interface import ICommand

class Console(object):
    def __init__(self, name, config_path=None, service_config_paths=[]):
        self.name      = name
        self.container = Core()

        self.config = {}

        if config_path:
            with open(config_path) as f:
                self.config.update(json.load(f))

            if 'db' in self.config:
                self._prepare_db_connections()

        self.container.load(*service_config_paths)

    def activate(self):
        sequence = [
            ('services', self._use_imagination),
            ('imports',  self._import_commands),
        ]

        main_parser = argparse.ArgumentParser(self.name)
        subparsers  = main_parser.add_subparsers(help='sub-commands')

        services = {}

        for key, action in sequence:
            if key in self.config and self.config[key]:
                services.update(
                    action(
                        subparsers,
                        self.config[key]
                    )
                )

        if not services:
            print('No commands available')
            return

        args = main_parser.parse_args()

        try:
            args.func(args)
        except AttributeError as e:
            main_parser.print_help()

            return

    def _use_imagination(self, subparsers, enabled):
        services = {}

        for identifier, service in self._get_interface_containers():
            self._register_command(
                subparsers,
                identifier,
                type(service),
                service
            )

            services[identifier] = service

        return services

    def _import_commands(self, subparsers, module_paths):
        classes  = []
        services = {}

        for module_path in module_paths:
            try:
                module = importlib.import_module(module_path)

                classes.extend(self._retrieve_command_classes(module))
            except ImportError as e:
                parts = re.split('\.', module_path)

                alternative_path = '.'.join(parts[:-1])
                class_name       = parts[-1]

                if not alternative_path:
                    raise RuntimeError('Unable to import {}'.format(module_path))

                module = importlib.import_module(alternative_path)
                cls    = self._get_command_class(module, class_name)

                classes.append(cls)

        for CommandClass in classes:
            sub_cli    = CommandClass()
            identifier = sub_cli.identifier()

            self._register_command(
                subparsers,
                identifier,
                CommandClass,
                sub_cli
            )

            services[identifier] = sub_cli

        return services

    def _retrieve_command_classes(self, module):
        classes = []

        for property_name in dir(module):
            if '_' in property_name[0]:
                continue

            ClassType = self._get_command_class(module, property_name)

            if ClassType == ICommand:
                continue

            if not issubclass(ClassType, ICommand):
                continue

            classes.append(ClassType)

        return classes

    def _register_command(self, subparsers, identifier, cls, instance):
        documentation  = cls.__doc__
        command_parser = subparsers.add_parser(identifier, help=documentation)

        instance.define(command_parser)
        command_parser.set_defaults(func=instance.execute)

    def _get_command_class(self, module, property_name):
        return eval('module.{}'.format(property_name))

    def _get_interface_containers(self):
        identifiers = self.container.all()

        for identifier in identifiers:
            service = self.container.get(identifier)

            if not isinstance(service, ICommand):
                continue

            yield identifier, service

    def _prepare_db_connections(self):
        db_config       = self.config['db']
        manager_config  = db_config['managers']
        service_locator = self.container.locator
        em_factory      = service_locator.get('db')

        for alias in manager_config:
            url = manager_config[alias]['url']

            em_factory.set(alias, url)

            def callback(em_factory, db_alias):
                return em_factory.get(db_alias)

            callback_proxy = CallbackProxy(callback, em_factory, alias)

            service_locator.set('db.{}'.format(alias), callback_proxy)
