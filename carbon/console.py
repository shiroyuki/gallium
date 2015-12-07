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

import .core import Core

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
        main_parser = argparse.ArgumentParser(self.name)
        subparsers  = main_parser.add_subparsers(help='sub-commands')

        for identifier in self.container.all():
            service = self.container.get(identifier)

            if not isinstance(service, ICommand):
                continue

            documentation  = type(service).__doc__
            command_parser = subparsers.add_parser(identifier, help=documentation)

            service.define(command_parser)

            command_parser.set_defaults(func=service.execute)

        args = main_parser.parse_args()
        args.func(args)

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
