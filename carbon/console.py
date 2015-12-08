""" Prototype for Tori 4.0+ and Imagination 1.10+

    :Author: Juti Noppornpitak
"""

import argparse
from contextlib import contextmanager
import json

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
            ('use_imagination',   self._use_imagination),
            ('auto_import_paths', self._auto_import_paths),
        ]

        for key, action in sequence:
            if key in self.config and self.config[key]:
                action()

    def _use_imagination(self):
        has_interface_containers = False

        main_parser = argparse.ArgumentParser(self.name)
        subparsers  = main_parser.add_subparsers(help='sub-commands')

        for service in self._get_interface_containers():
            documentation  = type(service).__doc__
            command_parser = subparsers.add_parser(identifier, help=documentation)

            service.define(command_parser)

            command_parser.set_defaults(func=service.execute)

            has_interface_containers = True

        if not has_interface_containers:
            print('No commands available')
            return

        args = main_parser.parse_args()
        args.func(args)

    def _auto_import_paths(self):
        mod = __import__()

    def _get_interface_containers(self):
        identifiers = self.container.all()

        for identifier in identifiers:
            service = self.container.get(identifier)

            if not isinstance(service, ICommand):
                continue

            yield service

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
