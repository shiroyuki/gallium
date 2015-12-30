"""
Carbon Core
###########

:Author: Juti Noppornpitak
"""

from contextlib import contextmanager

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer
from imagination.entity  import CallbackProxy
from imagination.entity  import Entity
from imagination.loader  import Loader
from imagination.locator import Locator

class Core(object):
    """ The Core of the Framework
    """
    def __init__(self, locator=None):
        self.locator     = locator or Locator()
        self.transformer = Transformer(self.locator)
        self.assembler   = Assembler(self.transformer)

        self.default_services = []
        self.cache_map        = None

        self._register_default_services()

    @contextmanager
    def passive_mode(self):
        self.assembler.activate_passive_loading()
        yield
        self.assembler.deactivate_passive_loading()

    def get(self, id):
        return self.locator.get(id)

    def load(self, *paths):
        with self.passive_mode():
            [
                self.assembler.load(path)
                for path in paths
            ]

            self.cache_map = None

    def all(self):
        if not self.cache_map:
            self.cache_map = {
                i: self.locator.get(i)
                for i in self.locator.entity_identifiers
            }

        return self.cache_map

    def _register_default_services(self):
        for entity_id, package_path, args, kwargs in self.default_services:
            try:
                entity = self._create_entity(entity_id, package_path, *args, **kwargs)

                self.locator.set(entity_id, entity)
            except ImportError as exception:
                if entity_id == "db":
                    self.logger.info('Ignored {} as package "passerine" is neither available or loadable (containing errors).'.format(package_path))

                    continue

                raise ImportError('Failed to register {} ({})'.format(entity_id, package_path))

    def _create_entity(self, id, package_path, *args, **kwargs):
        loader = Loader(package_path)

        return Entity(id, loader, *args, **kwargs)
