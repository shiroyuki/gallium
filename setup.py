import os
import sys

version      = '0.8.0'
primary_cmd  = 'bin/gallium'
shortcut_cmd = 'bin/g{version}'.format(version = sys.version_info.major)
install_cmds = [primary_cmd]

if os.path.exists(shortcut_cmd):
    install_cmds.append(shortcut_cmd)

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name         = 'gallium',
    version      = version,
    description  = 'A micro CLI development framework',
    license      = 'MIT',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'https://github.com/shiroyuki/carbon',
    packages     = [
        'gallium',
        'gallium.cli',
        'gallium.ext',
        'gallium.loader',
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    scripts          = install_cmds,
    install_requires = ['imagination', 'kotoba']
)
