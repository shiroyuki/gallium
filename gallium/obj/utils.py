from typing import Type, Tuple, Any

NONE_TYPE = type(None)


def stringify(obj):
    attrs = [
        f'{attr_name}={getattr(obj, attr_name)}'
        for attr_name in dir(obj)
        if attr_name[0] != '_' and not callable(getattr(obj, attr_name))
    ]

    return f'{type(obj).__module__}.{type(obj).__name__}({", ".join(attrs)})'


def is_optional(annotation: Type):
    if hasattr(annotation, "__args__"):
        unioned_types = getattr(annotation, "__args__")
        return NONE_TYPE in unioned_types
    return False


def get_all_types(annotation: Type) -> Tuple[Type]:
    if hasattr(annotation, "__args__"):
        return tuple(unioned_type
                     for unioned_type in getattr(annotation, "__args__")
                     if unioned_type != NONE_TYPE)
    return (annotation,)


def is_dataclass_class(cls: Type):
    return hasattr(cls, '__dataclass_fields__')
