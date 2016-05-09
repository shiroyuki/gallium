import re
import sys

from imagination.entity        import CallbackProxy, ReferenceProxy
from imagination.exception     import UnknownEntityError
from imagination.factorization import Factorization
from imagination.locator       import Locator

from ..interface   import ICommand, alias
from ..helper      import Reflector

class EntityManagementCommand(object):
    def get_id_to_wrapper_map(self):
        locator     = self.core.locator
        identifiers = locator.entity_identifiers
        wrapper_map  = {}

        for identifier in identifiers:
            wrapper = locator.get_wrapper(identifier)

            kind = self.get_wrapped_class(wrapper)

            wrapper_map[identifier] = kind

        return wrapper_map

    def get_class(self, wrapper):
        return Locator \
            if isinstance(wrapper, Locator) \
            else wrapper.loader.package

    def get_wrapped_class(self, wrapper):
        if isinstance(wrapper, Locator):
            return Locator
        elif hasattr(wrapper, 'loader'):
            return wrapper.loader.package
        elif isinstance(wrapper, Factorization):
            return Factorization
        elif type(wrapper) in (CallbackProxy, ReferenceProxy):
            return Factorization

        raise RuntimeError('Failed to retrieve the wrapper class.')

@alias('services')
class EntityList(ICommand, EntityManagementCommand):
    """ List all the registered entities/services. """
    def identifier(self):
        return 'services.list'

    def define(self, parser):
        pass

    def execute(self, args):
        wrapper_map = self.get_id_to_wrapper_map()
        identifiers = list(wrapper_map.keys())

        max_id_length = max([len(id) for id in identifiers])
        max_cn_length = max([len(Reflector.fqcn(wrapper_map[id])) for id in identifiers])

        row_template = '{sid:<' + str(max_id_length) + '} {cn}'

        print()
        print(row_template.format(sid = 'Service', cn = 'Class'))
        print(' '.join(['-' * max_id_length, '-' * max_cn_length]))

        identifiers.sort()

        for id in identifiers:
            print(row_template.format(
                sid = id,
                cn  = Reflector.fqcn(wrapper_map[id])
            ))

        print('\nMore details with "g3 services.show <Service ID>"\n')

@alias('doc')
class EntityShow(ICommand, EntityManagementCommand):
    """ Show short description of given entity/service IDs. """
    def identifier(self):
        return 'services.show'

    def define(self, parser):
        parser.add_argument('id', help = 'Service ID', nargs = '+')

    def execute(self, args):
        ids = args.id

        if not isinstance(ids, list):
            self._show_details(ids)
            return

        for id in ids:
            self._show_details(id)

    def _show_details(self, id):
        try:
            wrapper = self.core.locator.get_wrapper(id)
        except UnknownEntityError as e:
            message = str(e)
            message = message[0].lower() + (message[1:] if len(message) > 1 else '')

            print('Cannot retrieve the short documentation as {}'.format(message))

            sys.exit(1)

        cls = self.get_class(wrapper)

        # Title
        print('\n+{breaker}+\n| {sid} |\n+{breaker}+'.format(
            sid = id,
            breaker = '-' * (len(id) + 2)
        ))

        # Description
        documentation = Reflector.short_description(cls)
        default_doc   = '(No description available)'

        print(documentation or default_doc)

        print('\nMore details with "{cmd} {fqcn}"\n'.format(
            cmd = 'pydoc{}'.format(sys.version_info.major),
            fqcn = Reflector.fqcn(cls)
        ))
