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

This will install the supplied executables for both Python 3 and Python 2.7.

## Supplied Executables (BSD, Linux and Mac OS X Only)

* `gallium` and `g3` use Python 3 interpreter.
* `g2` uses Python 2.7 or whatever `python` is set to.

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

The supplied Gallium interface (`gallium`, `g2`, and `g3`) will read the
configuration files in the following order.

* /usr/local/gallium/etc/config.json (the system-wide config file)
* ~/.gallium/config.json (the user config file)
* ./cli.json (the local config file)

## Simplicity

As the goal is to allow developers to get started on writing what really matters
instead of implementing the setup like a digital janitor, the basic implementation
only requires the pure-old-Python class. For example, here is a basic command.

```python
# imaginary module name: sampleapp.cli
from gallium.interface import ICommand

class HelloWorld(ICommand):
    def identifier(self):
        return 'com.shiroyuki.gallium.hw'

    def define(self, parser):
        pass

    def execute(self, args):
        print('Howdy?')
```

Then, you can call this command by executing `gallium com.shiroyuki.gallium.hw`

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
check out the extentions for [Imagination Framework](tree/master/gallium/ext/imagination.py) and [Passerine ORM](tree/master/gallium/ext/passerine.py) with [Gallium Core](tree/master/gallium/core/Core.py)
