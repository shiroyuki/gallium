""" Integration Extension for Gallium Core and Imagination Framework """

import os

from ..interface import IExtension

class Extension(IExtension):
    def default_settings(self):
        return []

    def config_key(self):
        return 'services'

    def initialize(self, core, config):
        core.load(*[
            os.path.abspath(path)
            for path in config
        ])
