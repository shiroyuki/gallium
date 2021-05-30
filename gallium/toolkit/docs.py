"""
Provides a tool to simply generate a documentation from the source code.

.. note:: This is designed to work with Sphinx.

There are two command lines available from this module.

* ``python3 -m gallium.toolkit.docs setup`` for setting up the Sphinx docs.
* ``python3 -m gallium.toolkit.docs build`` for automatically compiling documentation from the source code and generating the static site.

To make sure that the build command works, you will need to update Sphinx's ``conf.py``.

1. Add the path of the target module to python path. See the top of conf.py on how to do it, for example::

    import os
    import sys
    sys.path.insert(0, os.path.abspath('..'))

2. Add ``sphinx.ext.autodoc`` to ``extensions``, for example::

    extensions = ['sphinx.ext.autodoc']

"""

import glob
import os
import re
import subprocess
from typing import Optional

from gallium.cli.core import console

RE_FS_DELIMITER = re.compile(r'[/|\\]')
RE_PY_EXT = re.compile(r'\.py$')


@console.simple_command
def setup(path: str):
    """ Set up a simple Sphinx doc project """
    os.chdir(path)
    subprocess.call(['sphinx-quickstart'])

    print("Please update conf.py.")
    print(" 1. Add the path of the target module to python path. See the top of conf.py on how to do it.")
    print(" 2. Add \"extensions = ['sphinx.ext.autodoc']\" to the config.")
    print("")
    print("After that, you then can use the \"build\" command to build the doc.")


@console.simple_command
def build(path_to_doc_source: str,
          path_to_doc_destination: str,
          module_name: str = None,
          source_dir: Optional[str] = None,
          full_build: Optional[bool] = False):
    """ Build the documentation """
    if full_build:
        subprocess.call(['rm', '-rvf', os.path.join(path_to_doc_destination, '*')])
        subprocess.call(['rm', '-rvf', os.path.join(path_to_doc_destination, '.*')])

    glob_string = os.path.join(module_name, '**', '*.py')

    if source_dir:
        glob_string = os.path.join(source_dir)

    sub_module_names = list()

    #################
    # Submodule Doc #
    #################
    for file_path in glob.glob(glob_string, recursive=True):
        sub_module_name = RE_FS_DELIMITER.sub(r'.', RE_PY_EXT.sub(r'', file_path))
        with open(os.path.join(path_to_doc_source, f'{sub_module_name}.rst'), 'w') as f:
            f.write(f"""
{sub_module_name}
{'=' * len(sub_module_name)}

.. automodule:: {sub_module_name}
   :members:
            """.strip())
        sub_module_names.append(sub_module_name)

    ##############
    # Index Page #
    ##############
    os.unlink(os.path.join(path_to_doc_source, 'index.rst'))
    index_toc = '\n   '.join(sorted([
        file_path[len(path_to_doc_source):]
        for file_path in glob.glob(os.path.join(path_to_doc_source, '**', '*.rst'), recursive=True)
    ]))
    with open(os.path.join(path_to_doc_source, 'index.rst'), 'w') as f:
        # language=ReStructuredText
        f.write(f"""
{module_name}
{'=' * len(module_name)}

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   {index_toc}

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
            """.strip())

    try:
        subprocess.call(['sphinx-build', '-b', 'html', path_to_doc_source, path_to_doc_destination])
    except Exception as e:
        raise IOError('Unable to build the doc')


if __name__ == '__main__':
    console.run_with()
