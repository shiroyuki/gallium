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
