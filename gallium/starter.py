import codecs
import json
import os
import sys

try:
    import yaml
except ImportError:
    pass

from gallium                    import Console, Core
from gallium.loader.basic       import Loader as BasicLoader
from gallium.loader.imagination import Loader as ImaginationLoader

base_path = os.path.abspath(os.getcwd())

global_base_path        = '/usr/local/gallium'
global_config_path      = os.path.join(global_base_path, 'etc')
global_config_file_path = os.path.join(global_config_path, 'config.json')
user_home_path          = os.getenv('GALLIUM_HOME') or ''

# On Windows, Gallium will not look into the user configuration.
if os.name != 'nt':
    default_user_home_path  = os.path.join(os.getenv('HOME'), '.gallium')
    user_home_path          = os.getenv('GALLIUM_HOME') or default_user_home_path

user_config_file_path = os.path.join(user_home_path, 'config.json')

symlinks = {
    global_config_path: '/etc/gallium',
}


def __p(path):
    intended_path = os.path.join(base_path, path)

    if not os.path.exists(intended_path):
        raise IOError('{} not exists'.format(intended_path))

    return intended_path


def __update_config(base_config, updating_config):
    required_sections = ('extensions', 'paths', 'services', 'imports', 'settings')

    for section in required_sections:
        is_settings   = section == 'settings'
        default_value = dict() if is_settings else list()

        extended_config = updating_config[section] \
            if section in updating_config \
            else None

        if not extended_config:
            continue

        if section not in base_config:
            base_config[section] = default_value

        section = base_config[section]

        if is_settings:
            section.update(extended_config)
        else:
            section.extend(extended_config)

    for section in updating_config:
        if section in required_sections:
            continue

        if section not in base_config:
            base_config[section] = updating_config[section]

            continue

        updated = updating_config[section]

        if isinstance(updated, list):
            for item in updated:
                base_config[section].append(item)

            continue

        elif isinstance(updated, dict):
            for item_key in updated:
                base_config[section][item_key] = updated[item_key]

            continue

        base_config[section] = updated


def __is_readable(path):
    return os.path.exists(path) and os.access(path, os.R_OK)


def __can_read_any_of(*paths):
    readable_paths = []

    for path in paths:
        if __is_readable(path):
            readable_paths.append(os.path.abspath(path))

    return readable_paths


def __get_default_readable_paths(default_file_name = None):
    override_config_path = os.getenv('GALLIUM_CONF') or os.getenv('GA_CONF')
    default_file_name    = default_file_name or 'cli'

    if override_config_path:
        local_config_path = override_config_path

        sys.stderr.write('Reading a configuration from {}'.format(local_config_path))
    else:
        # Load configuration files from the default locations
        try:
            local_config_path = __p('{default_file_name}.json'.format(default_file_name = default_file_name))
        except IOError:
            try:
                local_config_path = __p('{default_file_name}.yml'.format(default_file_name = default_file_name))
            except IOError:
                raise IOError('Cannot find either {default_file_name}.json or {default_file_name}.yml'.format(default_file_name = default_file_name))

    seeking_config_files = [local_config_path, user_config_file_path, global_config_file_path]

    return __can_read_any_of(*seeking_config_files)


def load_config(readable_file_paths = None, default_file_name = None):
    # Ensure that the base path is at the top of the Python paths.
    if base_path not in sys.path:
        sys.path.insert(0, base_path)

    cli_config = {}

    readable_file_paths = readable_file_paths or __get_default_readable_paths(default_file_name)

    if not readable_file_paths:
        raise IOError('The configuration files are not defined.')

    for readable_file_path in readable_file_paths:
        with codecs.open(readable_file_path, 'r') as f:
            if readable_file_path[-4:] == '.yml':
                if 'yaml' not in sys.modules:
                    raise ImportError('You must install pyyaml before using a YAML configuration.')

                file_cli_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
            else:
                file_cli_config = json.load(f)

            __update_config(
                cli_config,
                file_cli_config
            )

    # Extends Python paths.
    if 'paths' in cli_config:
        sys.path.extend(cli_config['paths'])

    return {
        'content': cli_config,
        'paths':   readable_file_paths,
    }


def main(config_content = None, readable_file_paths = None, default_file_name = None,
         default_extensions = None, default_commands = None):
    console_name = os.path.basename(sys.argv[0]) or __package__

    config = {
        'content': {
            'imports'    : [],
            'extensions' : [],
        }
    }

    if config_content:
        config['content'] = config_content
    else:
        try:
            config_from_files = load_config(readable_file_paths, default_file_name)

            config.update(config_from_files)
        except IOError as e:
            sys.stderr.write('WARNING: {}\n'.format(e))

    current_config = config['content']

    # Initialize the Gallium core.
    framework_core = Core()

    basic_loader = BasicLoader()

    enabled_loaders = [
        basic_loader,
    ]

    # Add the utility for Imagination framework.
    if not default_commands:
        default_commands = [
            'gallium.cli.imagination',
            'gallium.cli.setup',
        ]

    if not default_extensions:
        default_extensions = []

    try:
        for default_command in default_commands:
            current_config['imports'].insert(0, default_command)
    except KeyError:
        sys.stderr.write('ERROR: Failed to register default commands\n')
        sys.exit(1)

    try:
        for default_extension in default_extensions:
            current_config['extensions'].insert(0, default_extension)
    except KeyError:
        sys.stderr.write('ERROR: Failed to register default extensions\n')
        sys.exit(1)

    # Create a console interface.
    console = Console(
        name    = console_name,
        core    = framework_core,
        config  = current_config,
        loaders = enabled_loaders
    )

    console.activate()
