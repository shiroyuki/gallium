import datetime
from abc import ABC
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, List, Optional


class PlugIn(ABC):
    def can_handle(self, obj: Any) -> bool:
        ...

    def encode(self, obj: Any) -> Any:
        ...


class DataClassPlugIn(PlugIn):
    def can_handle(self, obj: Any) -> bool:
        return is_dataclass(obj)

    def encode(self, obj: Any) -> Any:
        return asdict(obj)


class DateTimePlugIn(PlugIn):
    def __init__(self, time_format: Optional[str] = None):
        self.__time_format = time_format

    def can_handle(self, obj: Any) -> bool:
        return isinstance(obj, datetime.datetime)

    def encode(self, obj: datetime.datetime) -> Any:
        return obj.strftime(self.__time_format) if self.__time_format else obj.isoformat()


class EnumPlugIn(PlugIn):
    def can_handle(self, obj: Any) -> bool:
        return isinstance(obj, Enum)

    def encode(self, obj: Enum) -> Any:
        return obj.value


class ObjectEncoder:
    def __init__(self):
        self.__plug_ins: List[PlugIn] = []

    def register(self, plug_in: PlugIn):
        self.__plug_ins.append(plug_in)
        return self

    def encode(self, obj: Any):
        for plug_in in self.__plug_ins:
            if plug_in.can_handle(obj):
                return self.encode(plug_in.encode(obj))

        if isinstance(obj, dict):
            return {
                k: self.encode(v)
                for k, v in obj.items()
            }

        if not isinstance(obj, str) and hasattr(obj, '__iter__'):
            return [
                self.encode(item)
                for item in obj
            ]

        return obj

    @staticmethod
    def build():
        return ObjectEncoder() \
            .register(DataClassPlugIn()) \
            .register(DateTimePlugIn()) \
            .register(EnumPlugIn())
