import contextlib
import os
import re


@contextlib.contextmanager
def work_from(temporary_working_dir):
    origin = os.getcwd()

    os.chdir(temporary_working_dir)
    yield
    os.chdir(origin)


class Reflector(object):
    re_newline      = re.compile('(\r?\n){2,}')
    re_extra_spaces = re.compile('\s{2,}')

    @staticmethod
    def fqcn(cls):
        """ Get the fully-qualified class name.

            :param type cls: the class type

            :rtype: str
        """
        return '{}.{}'.format(cls.__module__, cls.__name__)

    @staticmethod
    def short_description(cls):
        """ Get the short description of the given class.

            :param type cls: the class type

            :rtype: str
        """
        documentation = cls.__doc__

        if not documentation:
            return None

        blocks = Reflector.re_newline.split(documentation.strip())

        return Reflector.re_extra_spaces.sub(' ', blocks[0])
