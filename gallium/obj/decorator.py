from typing import Type

from gallium.obj.utils import stringify


def to_string(cls: Type):
    cls.__str__ = stringify
    return cls
