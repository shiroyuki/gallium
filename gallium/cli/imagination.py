import re
import sys
from imagination.locator import Locator
from gallium.interface   import ICommand, alias
from gallium.helper      import Reflector

class EntityManagementCommand(object):
    # static property
    reflector = Reflector()

    def get_id_to_wrapper_map(self):
        locator     = self.core.locator
        identifiers = locator.entity_identifiers
        wrapper_map  = {}

        for identifier in identifiers:
            wrapper = locator.get_wrapper(identifier)
            kind    = Locator \
                if isinstance(wrapper, Locator) \
                else wrapper.loader.package

            wrapper_map[identifier] = kind

        return wrapper_map

    def get_class(self, wrapper):
        return Locator \
            if isinstance(wrapper, Locator) \
            else wrapper.loader.package

@alias('services')
class EntityList(ICommand, EntityManagementCommand):
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

        for id in identifiers:
            print(row_template.format(
                sid = id,
                cn  = Reflector.fqcn(wrapper_map[id])
            ))

        print('\nMore details with "g3 services.show <Service ID>"\n')

@alias('doc')
class EntityShow(ICommand, EntityManagementCommand):
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
        wrapper = self.core.locator.get_wrapper(id)
        cls     = self.get_class(wrapper)

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
