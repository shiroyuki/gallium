import sys
from dataclasses import dataclass
from getpass import getpass
from typing import Optional, Iterable, Dict


@dataclass
class Field:
    name: str
    label: Optional[str]
    value: str
    sensitive: bool
    required: bool
    default: str

    @staticmethod
    def build(name: str, label: Optional[str] = None, sensitive: Optional[bool] = False, required: Optional[bool] = True, default: Optional[str] = None):
        return Field(
            name=name,
            label=label or name,
            value=None,
            sensitive=sensitive,
            required=required,
            default=default,
        )


class Form:
    def __init__(self, fields: Iterable[Field], max_retry_count: int = 3):
        self.__max_retry_count = max_retry_count
        self.__fields: Iterable[Field] = fields

    def prompt(self):
        for field in self.__fields:
            prompt_user_for = getpass if field.sensitive else input

            remaining_retry_count = self.__max_retry_count
            value: Optional[str] = None

            while not value and field.required:
                if remaining_retry_count <= 0:
                    sys.stderr.write('<<< ERROR: You still have not given the valid input. Self-terminated for now '
                                     'but you may rerun this command later.\n')
                    raise IOError('Invalid input for ' + field.label)
                if remaining_retry_count < self.__max_retry_count:
                    sys.stderr.write('<<< WARNING: The input is invalid. Please try again.\n')
                remaining_retry_count -= 1
                value = prompt_user_for(f'>>> {field.label}: ')

            field.value = value or None

        return self

    def to_dict(self) -> Dict[str, str]:
        return {
            field.name: field.value
            for field in self.__fields
        }
