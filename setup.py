try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name         = 'carbon',
    version      = '0.1.0',
    description  = 'A micro CLI development framework',
    license      = 'MIT',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'https://github.com/shiroyuki/carbon',
    packages     = [
        'carbon',
        'carbon.loader',
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
    scripts          = ['bin/carbon'],
    install_requires = ['imagination', 'kotoba']
)
