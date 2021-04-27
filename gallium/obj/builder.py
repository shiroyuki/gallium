import inspect
from dataclasses import dataclass, is_dataclass
from typing import Type, Any, Dict, Tuple, List

from gallium.obj.utils import is_optional, get_all_types, is_dataclass_class


@dataclass(frozen=True)
class AttributeSpec:
    name: str
    types: Tuple[Type]
    optional: bool
    default: Any


@dataclass
class Attribute:
    spec: AttributeSpec
    value: Any
    initialized: bool

    def extract(self):
        if not self.spec.optional and not self.initialized:
            raise RequiredAttributeError(self.spec.name)

        return self.spec.default \
            if self.spec.optional and not self.initialized \
            else self.value


class ObjectBuilder:
    __HIDDEN_SCHEMA_PROPERTY_NAME = '__oriole_object_schema__'

    def __init__(self, cls: Type):
        self.__class = cls
        self.__class_schema: List[AttributeSpec] = list()
        self.__attribute_map: Dict[str, Attribute] = dict()
        self._analyze()

    def _analyze(self):
        # Reuse the cache.
        if hasattr(self.__class, self.__HIDDEN_SCHEMA_PROPERTY_NAME):
            self.__class_schema = getattr(self.__class, self.__HIDDEN_SCHEMA_PROPERTY_NAME)
        else:
            for attribute_name, annotation in self.__class.__annotations__.items():
                # Get the default value
                default_value = None
                if hasattr(self.__class, attribute_name):
                    class_attribute_value = getattr(self.__class, attribute_name)
                    if class_attribute_value is not None and not callable(class_attribute_value):
                        default_value = class_attribute_value

                # Add to the schema
                self.__class_schema.append(
                    AttributeSpec(name=attribute_name,
                                  types=get_all_types(annotation),
                                  optional=is_optional(annotation),
                                  default=default_value)

                )
            setattr(self.__class, self.__HIDDEN_SCHEMA_PROPERTY_NAME, self.__class_schema)

        if not hasattr(self.__class, '__annotations__'):
            raise IncompatibleBuildableClassError()

        for attr_spec in self.__class_schema:
            self.__attribute_map[attr_spec.name] = Attribute(
                spec=attr_spec,
                value=None,
                initialized=False,
            )

    def build(self, define_all_attributes: bool = True):
        """ Build an instance of the given class

            :param bool define_all_attributes: Flag to whether to fill in all attributes, including the ones which are
                                               not covered by the constructor.
        """
        properties = {
            attr.spec.name: attr.extract()
            for attr in self.__attribute_map.values()
        }

        if is_dataclass_class(self.__class):
            return self.__class(**properties)
        else:
            # Get the constructor parameters.
            constructor_signature = inspect.signature(self.__class)
            constructor_param_names = [param_name for param_name in constructor_signature.parameters]
            constructor_params = {
                param_name: properties[param_name]
                for param_name in constructor_param_names
            }

            # Instantiate the object.
            obj = self.__class(**constructor_params)

            if define_all_attributes:
                for attr_name, attr_value in properties.items():
                    setattr(obj, attr_name, attr_value)

            return obj

    def __getattr__(self, item):
        if item not in self.__attribute_map:
            raise AttributeError(f'No setter for {item}')

        def setter(value):
            self.__attribute_map[item].value = value
            self.__attribute_map[item].initialized = True
            return self

        return setter


class RequiredAttributeError(RuntimeError):
    pass


class IncompatibleBuildableClassError(RuntimeError):
    def __init__(self):
        super().__init__('Requires class annotations. '
                         'Check out the doc at https://github.com/shiroyuki/oriole/tree/master/oriole/docs.')
