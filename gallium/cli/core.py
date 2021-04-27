"""
This module is designed to speed up the development of command line apps without needing to specify arguments. The
arguments will be defined based on the signature of the decorated methods used to handle the command line input.

## Quick start

You can use the default `console` from `gallium.cli.core` or create your own.

For example, create `app.py` with the following source code.

```python
from gallium.cli.core import console

@console.command(["set", "config"])
def set_config(name: str):
    ''' Example to humanized command '''
    print(name)

@console.command("auth")
def authenticate(name: str):
    ''' Example to humanized command '''
    print(name)

@console.simple_command
def add(a: int, b: int):
    print(a + b)

console.run_with()
```

Then, you should be able to call `set_config`, `authenticate`, and `add` by invoking:

* `python3 app.py set config --name panda`
* `python3 app.py auth --name foo`
* `python3 app.py add --a 1 --b 2`

respectively.

"""
import importlib
import inspect
import logging
import re
from argparse import ArgumentParser
from typing import List, Optional, Callable, Union, Any, Dict, Type

from imagination.debug import get_logger

from gallium.obj.utils import is_optional, get_all_types


class Command:
    """ Command Metadata """
    def __init__(self, id: List[str], callable: Callable, description: Optional[str] = None):
        if len(id) == 0:
            raise ValueError(f'The command ID must be defined for {callable}.')

        self.__id = id
        self.__callable = callable
        self.__description = description

    @property
    def id(self) -> List[str]:
        return self.__id

    @property
    def description(self) -> Optional[str]:
        return self.__description

    @property
    def callable(self) -> Callable:
        return self.__callable

    def __repr__(self):
        return f'{type(self).__name__}({self.__callable.__module__}.{self.__callable.__name__})'

    def __str__(self):
        return f'{type(self).__name__}({self.__callable.__module__}.{self.__callable.__name__})'


class Console:
    """ Console (Argument Parser Wrapper) """
    __SPECIAL_PARSER_KEY_FOR_COMMAND = '_command'

    def __init__(self):
        self.__commands: List[Command] = list()
        self.__log = get_logger(type(self).__name__, logging.INFO)

    def command(self, id: Union[None, str, List[str]] = None, description: Optional[str] = None):
        """ A decorator to define a command

            .. warning:: This only works on static methods or functions.
        """
        def inner(_func: Callable):
            actual_id = (re.split(r'\s+', id) if isinstance(id, str) else id) if id else [_func.__name__]
            self.__commands.append(Command(actual_id,
                                           _func,
                                           (description or _func.__doc__ or '').lstrip()))
            return _func
        return inner

    def simple_command(self, _func: Callable):
        self.__commands.append(Command([_func.__name__],
                                       _func,
                                       (_func.__doc__ or '').lstrip()))
        return _func

    def run_with(self, *import_paths):
        for import_path in import_paths:
            importlib.import_module(import_path)
        parser_map = dict()
        for command in self.__commands:
            self.__compute_graph(command, parser_map, command.id)
        parser = ArgumentParser()
        self.__initialize_parser(parser, parser_map)
        args = parser.parse_args()

        params = {
            k: v
            for k, v in vars(args).items()
            if k not in ('func', 'origin_')
        }

        if hasattr(args, 'origin_'):
            command: Command = args.origin_
            self.__log.debug('command: %s -> %s (begin)', command, params)
            command.callable(**params)
            self.__log.debug('command: %s -> %s (end)', command, params)
        else:
            self.__log.error('Unable to process')
            parser.print_help()

    def __compute_graph(self, command, node: Dict[str, Any], id_trail: List[str]):
        command_block_name = id_trail[0]
        if command_block_name not in node:
            node[command_block_name] = dict()
        if len(id_trail) == 1:
            if self.__SPECIAL_PARSER_KEY_FOR_COMMAND in node[command_block_name]:
                already_registered_command = node[command_block_name][self.__SPECIAL_PARSER_KEY_FOR_COMMAND]
                raise RuntimeError(f'The command ID "{" ".join(command.id)}" has already been defined for {already_registered_command}')
            else:
                node[command_block_name][self.__SPECIAL_PARSER_KEY_FOR_COMMAND] = command
        else:
            self.__compute_graph(command, node[command_block_name], id_trail[1:])

    def __initialize_parser(self, parser: ArgumentParser, parser_map: Dict[str, Any], prefix_trail: Optional[List[str]] = None):
        prefix_trail = prefix_trail or list()
        subparsers = parser.add_subparsers()

        if self.__SPECIAL_PARSER_KEY_FOR_COMMAND in parser_map:
            # Define the registered command
            command: Command = parser_map[self.__SPECIAL_PARSER_KEY_FOR_COMMAND]
            parser.description = command.description
            parser.set_defaults(
                origin_=command,
                func=command.callable
            )
            self.__define_arguments(parser, command)
        else:
            # Define the default command (to provide sublisting)
            parser.set_defaults(func=lambda: parser.print_help())

        for sub_command_name, subparser_map in parser_map.items():
            if sub_command_name != self.__SPECIAL_PARSER_KEY_FOR_COMMAND:
                self.__initialize_parser(
                    subparsers.add_parser(sub_command_name),
                    subparser_map,
                    prefix_trail + [sub_command_name]
                )

    def __define_arguments(self, parser: ArgumentParser, command: Command):
        """ Define the command line argument based on the reflection of the callable.

            .. warning:: This does not support instance methods at the moment.
        """
        signature = inspect.signature(command.callable)
        for parameter_name, parameter in signature.parameters.items():
            self.__define_argument(parser, ' '.join(command.id), parameter_name, parameter)

    def __define_argument(self, parser: ArgumentParser, command_name: str, parameter_name: str, parameter: inspect.Parameter):
        """ Define the command line argument according to the given parameter

            .. warning:: This is still incomplete in term of handling any combination of type hints.
        """
        name = f'--{re.sub("_", "-", parameter_name)}'
        parameter_type = None
        required = True

        annotation = parameter.annotation

        # Determine whether the parameter is option.
        if hasattr(annotation, "__origin__"):
            annotated_type = getattr(annotation, "__origin__")
            required = is_optional(annotation)
            parameter_type = get_all_types(annotation)[0]

        if not parameter_type:
            parameter_type = annotation if annotation != inspect._empty else str

        description = f"{'' if required else '[Optional] '}({parameter_type}) {re.sub('_+', ' ', parameter_name)}"

        parser.add_argument(name, type=parameter_type, required=required, help=description)


console: Console = Console()
""" Default/Standalone Console """
