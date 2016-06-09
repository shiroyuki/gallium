"""
Carbon Interfaces
#################

:Author: Juti Noppornpitak

This is similar to controllers.
"""

import sys
import time

alias_property_name = '__gallium_cli_aliases__'

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

    def ask(self, message, choices = None, default = None, repeat_limit = None):
        """ Ask for response.
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

            if choices and response.lower() not in choices:
                error = 'Please respond with "{}".'.format('" or "'.join(choices))
                continue

            error = None
            break

        if error:
            print(error)
            sys.exit(1)

        if default is None and not response:
            print('Your response cannot be empty.')
            sys.exit(1)

        return response

    def stand_by(self, message, delay, on_sigint = None):
        """ Stand by and wait until the user sends SIGINT via keyboard.
        """
        print(message)

        try:
            time.sleep(delay)
        except KeyboardInterrupt as e:
            if on_sigint:
                if not callable(on_sigint):
                    raise RuntimeError('The callback handler must be callable.')

                on_sigint()

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
    def make_alias(cls):
        if not hasattr(cls, alias_property_name):
            setattr(cls, alias_property_name, set())

        for name in names:
            getattr(cls, alias_property_name).add(name)

        return cls

    return make_alias
