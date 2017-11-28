import json

from imagination.loader import Loader

from ..interface import IExtension, fetch_extension_dependencies

class InvalidExtensionError(ValueError): pass

class UnmatchedSettingTypeError(TypeError): pass

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

    activated_classes = set()

    for extension_fqcn in extension_fqcns:
        __activate_one_extension(core, config, Loader(extension_fqcn).package, activated_classes)

def __activate_one_extension(core, config : dict, extension_class : type, activated_classes : set):
    if not issubclass(extension_class, IExtension):
        raise ValueError('{} is not a subclass of {}.'.format(
            extension_class.__name__,
            IExtension.__name__
        ))

    if extension_class in activated_classes:
        return

    # Activate the depending extensions first.
    for depending_class in fetch_extension_dependencies(extension_class):
        __activate_one_extension(core, config, depending_class, activated_classes)

    activated_classes.add(extension_class)

    extension  = extension_class()
    config_key = extension.config_key()

    if config_key is None:
        # NOTE the extension will run without configuration.
        extension.initialize(core)

        return

    # NOTE the extension will run with configuration. Please note
    #      that the default settings may be used.
    default_settings = extension.default_settings()

    ext_config = config[config_key] \
        if config_key in config \
        else None

    setting_type = type(default_settings)

    if ext_config and not isinstance(ext_config, setting_type):
        raise UnmatchedSettingTypeError('{}.{} expected the settings to be of type {}, given {} instead.'.format(
            extension_class.__module__,
            extension_class.__name__,
            setting_type.__name__,
            ext_config
        ))
    elif not ext_config:
        ext_config = default_settings # Set to the default settings

    if isinstance(default_settings, dict):
        for key, value in default_settings.items():
            if key in ext_config:
                continue

            ext_config[key] = value # Set to the default value if not available

    extension.initialize(core, ext_config)
