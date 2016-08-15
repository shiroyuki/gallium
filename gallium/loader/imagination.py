from .common import ILoader
from ..interface import ICommand


class Loader(object):
    """ The default loader integrated with the core of the framework.

        TODO update this to be compatible with Imagination 2.
    """
    def __init__(self, core):
        self.core = core

    def configuration_section_name(self):
        return 'services'

    def all(self, imagination_config):
        for identifier in self.core.all():
            service = self.core.get(identifier)

            if not isinstance(service, ICommand):
                continue

            yield (identifier, type(service), service)
