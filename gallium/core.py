"""
Carbon Core
###########

:Author: Juti Noppornpitak
"""

from contextlib import contextmanager

from imagination.assembler.core  import Assembler
from imagination.meta.container  import Entity, Factorization, Lambda
from imagination.meta.definition import DataDefinition


class Core(object):
    """ The Core of the Framework

        This relies on Imagination Framework.
    """
    def __init__(self, locator=None):
        self.assembler = Assembler()

    @property
    def _core(self):
        return self.assembler.core

    def get(self, id):
        """ Get the service container. """
        return self._core.get(id)

    def load(self, *paths):
        """ Load service containers from multiple configuration files. """
        self.assembler.load(*paths)

    def all(self):
        if not self._cache_map:
            self._cache_map = {
                i: self.locator.get(i)
                for i in self.locator.entity_identifiers
            }

        return self._cache_map

    def set_entity(self, entity_id, fqcn):
        container = Entity(identifier = entity_id, fqcn = fqcn)

        self._core.update_metadata({entity_id: container})

    def set_factorization(self, entity_id, factory_id, factory_method_name):
        container = Factorization(entity_id, factory_id, factory_method_name)

        self._core.update_metadata({entity_id: container})

    def set_entity_param(self, entity_id, kind, value,
                         transformation_required = False, name = None):
        definition = DataDefinition(value, name, kind, transformation_required)
        metadata   = self._core.get_metadata(entity_id)

        metadata.params.add(definition, name)
