# Gallium - A Micro CLI Framework for Python

**Gallium Framework** is designed to eliminate the need of setting up bootstrap
and allow fast-pace CLI development where it only relies on built-in libraries
such as `ArgumentParser` to let the developers define the argument in the way
commonly known to any Python developers without asking them to learn new things.

So, the user can use run `gallium <sub-command> [...]` where the subcommands are
imported and defined in `cli.json` from the current working directory.

To override the default path of the configuration file, just run as
`GALLIUM_CONF=/path/to/config/anyname.json gallium ...`.

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
    ]
}
```

The name of each subcommand is defined by either `ICommand.identifier()` for any
commands via the basic setup or the ID of the command entity defined in the setup
with Imagination Framework (the `identifier` method will be ignored in this type
of setup).

## Simplicity

As the goal is to allow developers to get started on writing what really matters
instead of implementing the setup like a digital janitor, the basic implementation
only requires the pure-old-Python class. For example, here is a basic command.

```python
# imaginary module name: sampleapp.cli
from gallium.interface import ICommand

class HelloWorld(ICommand):
    def identifier(self, args):
        return 'com.shiroyuki.gallium.hw'

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
