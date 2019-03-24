import os
import sys

_minimum_version = (3, 5)

if sys.version_info < _minimum_version:
    raise RuntimeError('Required Python {}'.format(
        '.'.join([str(i) for i in _minimum_version])
    ))

version      = '1.4.2'
primary_cmd  = 'bin/gallium'
shortcut_cmd = 'bin/g{version}'.format(version = sys.version_info.major)
install_cmds = [primary_cmd]

if os.path.exists(shortcut_cmd):
    install_cmds.append(shortcut_cmd)

from distutils.core import setup

setup(
    name         = 'gallium',
    version      = version,
    description  = 'A micro CLI development framework',
    license      = 'MIT',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'https://github.com/shiroyuki/gallium',
    packages     = [
        'gallium',
        'gallium.cli',
        'gallium.ext',
        'gallium.loader',
        'gallium.model',
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    scripts          = install_cmds,
    install_requires = [
        'kotoba',
        'imagination',
        'pyyaml',
    ],
    python_requires = '>=3.5',
)
