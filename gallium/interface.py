"""
Carbon Interfaces
#################

:Author: Juti Noppornpitak

This is similar to controllers.
"""

class ICommand(object):
    """ Command Interface """
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
