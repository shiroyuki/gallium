"""
Carbon Interfaces
#################

:Author: Juti Noppornpitak

This is similar to controllers.
"""

import sys
import time

alias_property_name = '__gallium_cli_aliases__'
extension_dependency_list_property_name = '__depending_extension_classes__'


class EmergencyExit(RuntimeError):
    """ Emergency Exit (the message is the exit code) """


class EmptyResponse(RuntimeError):
    """ Empty Response """


class ICommand(object):
    """ Subcommand Interface """
    @property
    def settings(self):
        return self.__settings

    @property
    def core(self):
        return self.__core

    def set_settings(self, settings):
        self.__settings = settings

    def set_core(self, core):
        self.__core = core

    def identifier(self):
        """ Define the identifier of the command.

            This will be overridden by the imagination entity ID if the command
            is loaded with the integration with Imagination Framework.

            :return: the identifier (ID) for the command
            :rtype: str
        """
        raise NotImplementedError()

    def define(self, parser):
        """ Define the arguments for this command.

            :param argparse.ArgumentParser parser: the argument parser of the command
            :return: nothing
        """
        raise NotImplementedError()

    def execute(self, args):
        """ The main method of the command
        """
        raise NotImplementedError()

    def ask(self, message, choices : dict = None, default = None,
            repeat_limit = None, kind : type = None, validate : callable = None):
        """ Ask for response.

            :param type kind:
                the type of the response
            :param callable validate:
                the callable to validate the input outside the simple restricting
                options. The callable must take only one parameter which is of
                the given data type (default to string). The callable also must
                return ``None`` or ``True`` on valid response. Otherwise, it must
                return ``False`` (generic error will be used) or raise AssertionError
                which the custom error message from the error object will be used.

            .. versionadded:: 1.1
               The parameters ``kind`` and ``validate`` are added.
        """
        blocks = [message]

        if not repeat_limit or repeat_limit < 1:
            repeat_limit = 1

        if choices:
            blocks.append('[{}]'.format('/'.join(choices)))

        if default:
            blocks.append('({})'.format(default))

        actual_prompt = '{}: '.format(' '.join(blocks))

        response = None
        error    = None

        for i in range(repeat_limit):
            response = input(actual_prompt) \
                if sys.version_info.major == 3 \
                else raw_input(actual_prompt)

            if not response:
                response = default

            kind(response) if kind and callable(kind) else response

            if choices and response.lower() not in choices:
                error = 'Please respond with "{}".'.format('" or "'.join(choices))

                continue

            try:
                if validate and not validate(response):
                    error = 'Invalid response'
            except AssertionError as e:
                error = str(e)

            error = None

            break

        if error:
            raise AssertionError(error)

        if default is None and not response:
            raise EmptyResponse('Your response cannot be empty.')

        return response

    def stand_by(self, message, delay, on_sigint = None):
        """ Stand by and wait until the user sends SIGINT via keyboard. """
        print(message)

        try:
            time.sleep(delay)
        except KeyboardInterrupt as e:
            if on_sigint:
                if not callable(on_sigint):
                    raise RuntimeError('The callback handler must be callable.')

                on_sigint()
            # endif

    def alert(self, message):
        sys.stderr.write('{}\n'.format(message))

    def bail_out(self, code = 1):
        raise EmergencyExit(code)

class IExtension(object):
    def default_settings(self):
        """ Extension's default settings

            This methos is only used to retrieve the default settings of the
            extension **ONLY IF** the configuration key is present.
        """
        raise ValueError('No settings, including the default one')

    def config_key(self):
        """ Configuration key

            If the configuration key is not present, i.e., ``None``, the extension
            will begin the initialization with a None object (a place holder).

            :rtype: str or None
        """
        raise NotImplementedError()

    def initialize(self, core, config = None):
        """ Initialize the extension from the console.

            :param gallium.core.Core core:   the Gallium core
            :param dict              config: the extension-specific configuration
        """
        raise NotImplementedError()

def alias(*names):
    """ Add the alias to the command """
    def make_alias(cls):
        if not hasattr(cls, alias_property_name):
            setattr(cls, alias_property_name, set())

        for name in names:
            getattr(cls, alias_property_name).add(name)

        return cls

    return make_alias

def depend_on(*extension_classes):
    """ Add the extension dependencies to an extension """
    def add_depending_extension(cls):
        if not hasattr(cls, extension_dependency_list_property_name):
            setattr(cls, extension_dependency_list_property_name, set())

        for extension_class in extension_classes:
            getattr(cls, extension_dependency_list_property_name).add(extension_class)

        return cls

    return add_depending_extension

def fetch_extension_dependencies(extension_class : type) -> set:
    if not hasattr(extension_class, extension_dependency_list_property_name):
        return set()

    return getattr(extension_class, extension_dependency_list_property_name)
