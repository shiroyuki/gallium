import os
from distutils.core import setup
import sys

_minimum_version = (3, 5)

if sys.version_info < _minimum_version:
    raise RuntimeError('Required Python {}'.format(
        '.'.join([str(i) for i in _minimum_version])
    ))

version = '2.0.0a4'

long_description = ''
if os.path.exists('readme.md'):
    with open('readme.md', "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name='gallium',
    version=version,
    description='A micro CLI development framework',
    license='MIT',
    author='Juti Noppornpitak',
    author_email='juti_n@yahoo.co.jp',
    url='https://github.com/shiroyuki/gallium',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'gallium',
        'gallium.cli',
        'gallium.obj',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'imagination~=3.3',
        'kotoba~=3.0',
        'pyyaml~=5.4.1',
    ],
    python_requires='>=3.5',
)
