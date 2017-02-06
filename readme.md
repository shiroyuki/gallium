# Gallium - A Micro CLI Framework for Python

**Gallium Framework** is designed to eliminate the need of setting up bootstrap
and allow fast-pace CLI development where it only relies on built-in libraries
such as `ArgumentParser` to let the developers define the argument in the way
commonly known to any Python developers without asking them to learn new things.

So, the user can use run `gallium <sub-command> [...]` where the subcommands are
imported and defined in `cli.json` from the current working directory.

To override the default path of the configuration file, just run as
`GA_CONF=/path/to/config/anyname.json gallium ...`.

Please remember that when you are in doubt, use the classic `-h` or `--help` to find out more.

## How to install

You can install either with PIP by executing `pip3 install gallium` or by using `setup.py`.

This will install the supplied executables for both Python 3.

**This only supports Python 3.4 or newer.**

## Supplied Executables

For UNIX, BSD, Linux and Mac OS X Only,
* `gallium` and `g3` use Python 3 interpreter.

For Windows, see the section regarding to Windows way below.

## Configuration

Here is the desired syntax.

```javascript
{
    "paths": [
        /* optional, additional python paths */
    ],
    "services": [
        /* optional, paths to the XML configuration for an Imagination Framework app

            This is the setup with Imagination Framework (https://github.com/shiroyuki/Imagination).
        */
    ],
    "imports": [
        /* optional, fully qualified class names, e.g., "sampleapp.cli.BasicHW"
            where the module name is "sampleapp.cli" and the class name is "BasicHW".

            This is the basic setup.
        */
    ],
    "settings": {
        /* optional, shared settings across all commands. */
    }
}
```

The name of each subcommand is defined by either `ICommand.identifier()` for any
commands via the basic setup or the ID of the command entity defined in the setup
with Imagination Framework (the `identifier` method will be ignored in this type
of setup).

See an example from [the sample folder](sample).

## How Gallium read configuration

The supplied Gallium interface (`gallium` and `g3`) will read the
configuration files in the following order.

* `/usr/local/gallium/etc/config.json` (the system-wide config file)
* `~/.gallium/config.json` (the user config file)
* `./cli.json` (the local config file)

## Simplicity

As the goal is to allow developers to get started on writing what really matters
instead of implementing the setup like a digital janitor, the basic implementation
only requires the pure-old-Python class. For example, here is a basic command.

```python
# imaginary module name: sampleapp.cli
from gallium.interface import ICommand

class HelloWorld(ICommand):
    def identifier(self):
        return 'hi'

    def define(self, parser):
        pass

    def execute(self, args):
        print('Howdy?')
```

Then, you can call this command by executing `gallium hi` or `g3 hi`.

## Prompt the user for input

### `gallium.interface.ICommand.ask(message, choices : dict = None, default = None, repeat_limit = None, kind : type = None, validate : callable = None)`

(Added in Version 1.0.0a4)

Ask the user for response.

The parameter `message` will is the message when the prompt is triggered. For example, suppose this is implemented in `g3 init`

```python
# in an ICommand instance
full_name = self.ask('What is the app name?')
```

Sample output:

```
$ g3 init
What is the app name?: ▌
```

The parameter `choices` is to limited user response to a certain set of possible answers.

```python
# in an ICommand instance
confirmation = self.ask(
    'Are you sure?',
    choices = ['yes', 'no']
)
```

Sample output:

```
$ g3 init
... (omitted) ...
Are you sure? [yes/no]: ▌
```

The parameter `default` is the default response.

```python
# in an ICommand instance
confirmation = self.ask(
    'Are you sure?',
    choices = ['yes', 'no'],
    default = 'no'
)
```

Sample output:

```
$ g3 init
... (omitted) ...
Are you sure? [yes/no] (no): ▌
```

The parameter `repeat_limit` is to allow the user to correct invalid response.
By default, there is no retry (`repeat_limit` is 1).

The parameter `kind` is the type of the response.

The parameter `validate` is the callable to validate the input outside the simple
restricting options. The callable must take only one parameter which is of the
given data type (default to string). The callable also must return ``None`` or
``True`` on valid response. Otherwise, it must return ``False`` (generic error
will be used) or raise AssertionError which the custom error message from
the error object will be used.

### `gallium.interface.ICommand.stand_by(self, message, delay, on_sigint = None)`

(Added in Version 1.0.0a4)

Stand by and wait until the user sends SIGINT via keyboard.


## Incorporating with Imagination Framework

Simply define an `ICommand` class as an entity, e.g.,

```xml
<imagination>
    <entity id="apple" class="sampleapp.cli.HellowWorld"/>
    <!-- ... -->
</imagination>
```

Then, you can call this command by executing `gallium apple`.

## Extend the core.

You can extend the core by implement `gallium.interface.IExtension`. Please
check out the extentions for [Imagination Framework](https://github.com/shiroyuki/gallium/blob/master/gallium/ext/imagination.py) and [Passerine ORM](https://github.com/shiroyuki/gallium/blob/master/gallium/ext/passerine.py) with [Gallium Core](https://github.com/shiroyuki/gallium/blob/master/gallium/core.py)

## Limitations

#### Limited supports on Windows

The support for **Windows 10** is added since **version 0.8**.

Please note that the command line will be installed but not usable as it is
designed to work with **Bash** or UNIX/BSD/Linux shell. It might work when
Microsoft releases the updates for Windows 10 with Bash.

Until then, you can create a Python script with the following code.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gallium.starter   import main

if __name__ == '__main__':
    main() # which requires "cli.json"

    # Alternatively you can pass a config dictionary like this:
    # main({
    #     'imports': [
    #         # ...
    #     ]
    # })
```
