"""
Carbon Interfaces
#################

:Author: Juti Noppornpitak

This is similar to controllers.
"""
class ICommand(object):
    def define(self, parser):
        pass

    def execute(self, args):
        raise NotImplementedError('Interface method')
