import re
import sys

from imagination.meta.container import Entity, Factorization, Lambda
from imagination.exception      import UnknownEntityError
from imagination.loader         import Loader

try:
    standalone_container_available = True
    from imagination.standalone import container as standalone_container
except ImportError:
    standalone_container_available = False

from ..interface import ICommand, alias
from ..helper    import Reflector


class EntityManagementCommand(object):
    def get_id_to_wrapper_map(self, locator):
        identifiers = locator.all_ids()
        wrapper_map = {}

        for identifier in identifiers:
            wrapper_map[identifier] = locator.get_metadata(identifier)

        return wrapper_map

    def get_class(self, wrapper):
        return Locator \
            if isinstance(wrapper, Locator) \
            else wrapper.loader.package

    def get_wrapped_class(self, wrapper):
        if isinstance(wrapper, Locator):
            return Locator

        if type(wrapper) is Entity:
            return Loader(wrapper.fqcn).package

        if type(wrapper) is Factorization:
            return Factorization

        if type(wrapper) in Lambda:
            return Lambda

        raise RuntimeError('Failed to retrieve the wrapper class.')


@alias('services')
class EntityList(ICommand, EntityManagementCommand):
    """ List all the registered entities/services. """
    def identifier(self):
        return 'services.list'

    def define(self, parser):
        pass

    def execute(self, args):
        print('----------------- BEGIN -----------------')
        print()

        if not self.core.container.in_proxy_mode():
            print('⎡⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎤')
            print('⎢ With the built-in container           ⎥')
            print('⎣⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎦')

            self._show(self.core.container)

        if not standalone_container.in_proxy_mode() and standalone_container_available:
            print()
            print('⎡⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎤')
            print('⎢ With imagination.standalone.container ⎥')
            print('⎣⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎦')

            self._show(standalone_container)

        print()
        print('------------------ END ------------------')

    def _show(self, locator):
        wrapper_map = self.get_id_to_wrapper_map(locator)
        identifiers = list(wrapper_map.keys())

        id_to_fqcn_map = {}

        for identifier in identifiers:
            wrapper = wrapper_map[identifier]
            fqcn    = None

            if type(wrapper) is Factorization:
                fqcn = '(Factorized with "{}" by "{}")'.format(wrapper.factory_method_name, wrapper.factory_id)
            elif type(wrapper) is Entity:
                fqcn = wrapper.fqcn
            elif type(wrapper) is Lambda:
                fqcn = wrapper.fq_callable_name

            id_to_fqcn_map[identifier] = fqcn

        if not identifiers:
            print()
            print('  ***** No service registered *****')

            return

        max_id_length = max([len(i) for i in identifiers])
        max_cn_length = max([len(id_to_fqcn_map[i]) for i in identifiers])

        row_template = '{sid:<' + str(max_id_length) + '} {cn}'

        print()
        print(row_template.format(sid = 'Service', cn = 'Class'))
        print(' '.join(['-' * max_id_length, '-' * max_cn_length]))

        identifiers.sort()

        for identifier in identifiers:
            print(row_template.format(
                sid = identifier,
                cn  = id_to_fqcn_map[identifier]
            ))
