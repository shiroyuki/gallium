import codecs
import json
import os
import sys

from gallium                    import Console, Core
from gallium.loader.basic       import Loader as BasicLoader
from gallium.loader.imagination import Loader as ImaginationLoader

base_path = os.path.abspath(os.getcwd())
global_config_path = '/etc/gallium'

def __p(path):
    return os.path.join(base_path, path)

def __update_config(base_config, updating_config):
    for section in ['paths', 'services', 'imports', 'settings']:
        extending_list = updating_config[section] if section in updating_config else []

        if not extending_list:
            continue

        if section not in base_config:
            base_config[section] = []

        base_config[section].extend(extending_list)
        base_config[section] = list(set(base_config[section]))

def main():
    global global_config_path # TODO include the global config

    if base_path not in sys.path:
        sys.path.insert(0, base_path)

    console_name = __package__ or sys.argv[0]
    local_config_path  = os.getenv('GALLIUM_CONF') or __p('cli.json')

    service_config_paths = []

    if not os.path.exists(local_config_path) or not os.access(local_config_path, os.R_OK):
        raise IOError('{} is not readable.'.format(local_config_path))

    with codecs.open(local_config_path, 'r') as f:
        pre_config = json.load(f)

    if 'paths' in pre_config:
        sys.path.extend(pre_config['paths'])

    if 'services' in pre_config:
        service_config_paths.extend([
            __p(service_config_path)
            for service_config_path in pre_config['services']
        ])

    framework_core = Core()
    framework_core.load(*service_config_paths)

    basic_loader       = BasicLoader()
    imagination_loader = ImaginationLoader(framework_core)

    enabled_loaders = [
        basic_loader,
        imagination_loader
    ]

    console = Console(
        name        = console_name,
        core        = framework_core,
        config_path = local_config_path,
        loaders     = enabled_loaders
    )

    console.activate()
