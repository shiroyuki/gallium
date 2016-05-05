import json

from imagination.loader import Loader

from ..interface import IExtension

class InvalidExtensionError(ValueError): pass

def activate(core, config):
    """ Activate/load the extensions

        :param gallium.core.Core core:   The Gallium Core
        :param dict              config: The Callium Configuration
    """
    extension_fqcns = config['extensions'] \
        if 'extensions' in config \
        else []

    # Default extensions.
    if 'gallium.ext.imagination.Extension' not in extension_fqcns:
        extension_fqcns.insert(0, 'gallium.ext.imagination.Extension')

    for extension_fqcn in extension_fqcns:
        extension_class = Loader(extension_fqcn).package

        if not issubclass(extension_class, IExtension):
            raise ValueError('{} is not a subclass of {}.'.format(
                extension_class.__name__,
                IExtension.__name__
            ))

        extension  = extension_class()
        config_key = extension.config_key()

        if config_key is None:
            # NOTE the extension will run without configuration.
            extension.initialize(core)
        else:
            # NOTE the extension will run with configuration. Please note
            #      that the default settings may be used.
            ext_config = config[config_key] \
                if config_key in config \
                else extension.default_settings()

            extension.initialize(core, ext_config)
