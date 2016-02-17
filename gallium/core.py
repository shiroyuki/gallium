"""
Carbon Core
###########

:Author: Juti Noppornpitak
"""

from contextlib import contextmanager

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer
# from imagination.entity  import CallbackProxy
from imagination.entity  import Entity
from imagination.loader  import Loader
from imagination.locator import Locator

class Core(object):
    """ The Core of the Framework

        This relies on Imagination Framework.
    """
    def __init__(self, locator=None):
        self.locator     = locator or Locator()
        self.transformer = Transformer(self.locator)
        self.assembler   = Assembler(self.transformer)

        self._cache_map = None

    @contextmanager
    def passive_mode(self):
        self.assembler.activate_passive_loading()
        yield
        self.assembler.deactivate_passive_loading()

    def get(self, id):
        """ Get the service container. """
        return self.locator.get(id)

    def load(self, *paths):
        """ Load service containers from multiple configuration files. """
        with self.passive_mode():
            [
                self.assembler.load(path)
                for path in paths
            ]

            self._cache_map = None

    def all(self):
        if not self._cache_map:
            self._cache_map = {
                i: self.locator.get(i)
                for i in self.locator.entity_identifiers
            }

        return self._cache_map

    def set_entity(self, entity_id, entity_fqcn, *args, **kwargs):
        try:
            entity = self._create_entity(entity_id, entity_fqcn, args, kwargs)

            self.locator.set(entity_id, entity)
        except ImportError as exception:
            raise ImportError('Failed to register {} ({})'.format(entity_id, entity_fqcn))

    def _create_entity(self, id, entity_fqcn, args, kwargs):
        loader = Loader(entity_fqcn)

        return Entity(id, loader, *args, **kwargs)
