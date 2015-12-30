import importlib
import inspect
import re

from .common import ILoader
from ..interface import ICommand

class Loader(ILoader):
    """ The default loader without the integration with the Imagination framework
    """
    def configuration_section_name(self):
        return 'imports'

    def all(self, module_paths):
        for module_path in module_paths:
            try:
                module = importlib.import_module(module_path)

                for cls in self._retrieve_command_classes(module):
                    yield self._logical_group(cls)
            except ImportError as e:
                parts = re.split('\.', module_path)

                alternative_path = '.'.join(parts[:-1])
                class_name       = parts[-1]

                if not alternative_path:
                    raise RuntimeError('Unable to import {}'.format(module_path))

                module = importlib.import_module(alternative_path)
                cls    = self._get_command_class(module, class_name)

                yield self._logical_group(cls)

    def _logical_group(self, cls):
        cli = cls()

        return (cli.identifier(), cls, cli)

    def _retrieve_command_classes(self, module):
        for property_name in dir(module):
            if '_' in property_name[0]:
                continue

            ClassType = self._get_command_class(module, property_name)

            if ClassType == ICommand:
                continue

            if not inspect.isclass(ClassType):
                continue

            if not issubclass(ClassType, ICommand):
                continue

            yield ClassType

    def _get_command_class(self, module, property_name):
        return eval('module.{}'.format(property_name))
