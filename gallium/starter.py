import codecs
import json
import os
import sys

from gallium                    import Console, Core
from gallium.loader.basic       import Loader as BasicLoader
from gallium.loader.imagination import Loader as ImaginationLoader

base_path = os.path.abspath(os.getcwd())

def __p(path):
    return os.path.join(base_path, path)

def main():
    if base_path not in sys.path:
        sys.path.append(base_path)

    console_name = __package__ or sys.argv[0]
    config_path  = os.getenv('GALLIUM_CONF') or __p('cli.json')

    service_config_paths = []

    with codecs.open(config_path, 'r') as f:
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
        config_path = config_path,
        loaders     = enabled_loaders
    )

    console.activate()
