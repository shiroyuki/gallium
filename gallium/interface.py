"""
Carbon Interfaces
#################

:Author: Juti Noppornpitak

This is similar to controllers.
"""
class ICommand(object):
    def identifier(self):
        """ Define the identifier of the command.

            This will be overridden by the imagination entity ID if the command
            is loaded with the integration with Imagination Framework.

            :return: the identifier (ID) for the command
            :rtype: str
        """
        raise NotImplementedError('Interface method')

    def define(self, parser):
        """ Define the arguments for this command.

            :param argparse.ArgumentParser parser: the argument parser of the command
            :return: nothing
        """
        raise NotImplementedError('Interface method')

    def execute(self, args):
        """ The main method of the command
        """
        raise NotImplementedError('Interface method')
