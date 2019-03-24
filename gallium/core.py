"""
Carbon Core
###########

:Author: Juti Noppornpitak
"""

from contextlib import contextmanager

from imagination.assembler.core  import Assembler
from imagination.meta.container  import Entity, Factorization, Lambda
from imagination.meta.definition import DataDefinition
from imagination.standalone      import container as standalone_container

from gallium.model.internal import ContainerMode, Internal


class Core(object):
    """ The Core of the Framework

        This relies on Imagination Framework.
    """
    def __init__(self, assembler = None):
        self.assembler = assembler or Assembler(standalone_container)

    @property
    def _core(self):
        return self.container

    @property
    def container(self):
        return self.assembler.core

    def get(self, id):
        """ Get the service container. """
        return self._core.get(id)

    def load(self, *paths):
        """ Load service containers from multiple configuration files. """
        self.assembler.load(*paths)

    def set_entity(self, entity_id, fqcn):
        """ Register a new entity.

            .. deprecated:: 1.4.0
        """
        container = Entity(identifier = entity_id, fqcn = fqcn)

        self._core.update_metadata({entity_id: container})

    def set_factorization(self, entity_id, factory_id, factory_method_name):
        """ Register a new entity with factorization.

            .. deprecated:: 1.4.0
        """
        container = Factorization(entity_id, factory_id, factory_method_name)

        self._core.update_metadata({entity_id: container})

    def set_lambda(self, entity_id, import_path):
        """ Register a new lambda entity.

            .. deprecated:: 1.4.0
        """
        container = Lambda(entity_id, import_path)

        self._core.update_metadata({entity_id: container})

    def set_entity_param(self, entity_id, kind, value,
                         transformation_required = False, name = None):
        """ Define a constructor parameter for a particular entity.

            .. deprecated:: 1.4.0
        """
        definition = DataDefinition(value, name, kind, transformation_required)
        metadata   = self._core.get_metadata(entity_id)

        metadata.params.add(definition, name)

    def inject_entity_dependency(self, entity_id, dependency_id, name = None):
        """ Inject an entity as a dependency to the specified entity.

            .. deprecated:: 1.4.0
        """
        self.set_entity_param(entity_id, 'entity', dependency_id, True, name)

    def inject_entity_classinfo(self, entity_id, fqcn, name = None):
        """ Inject a class/type as a dependency to the specified entity.

            .. deprecated:: 1.4.0
        """
        self.set_entity_param(entity_id, 'class', fqcn, True, name)

    def configure(self, internal_config : Internal):
        # Handle the container mode.
        assert ContainerMode.is_valid(internal_config.container), \
            'The container mode MUST be one of {}, not {}. {}'.format(
                ', '.join(ContainerMode.valid_modes()),
                internal_config.container,
                ContainerMode.__doc__,
            )
