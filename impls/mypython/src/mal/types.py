"""Mal Types"""

from enum import Enum


class MalType(Enum):
    """Mal Type"""

    ATOM = "ATOM"
    FLOAT = "FLOAT"
    FUNCTION = "FUNCTION"
    HASHMAP = "HASHMAP"
    INTEGER = "INTEGER"
    KEYWORD = "KEYWORD"
    LIST = "LIST"
    STRING = "STRING"
    SYMBOL = "SYMBOL"
    VECTOR = "VECTOR"


class MalObject:
    """Mal Object"""

    def __init__(self, mal_type, value):
        self._mal_type = mal_type
        self._value = value

    def __repr__(self):
        return f"MalObject({self._mal_type}, {self._value})"

    @property
    def mal_type(self):
        """Mal Type"""
        return self._mal_type

    @property
    def value(self):
        """Value"""
        return self._value


# Special objects
true = MalObject(MalType.SYMBOL, "true")
false = MalObject(MalType.SYMBOL, "false")
nil = MalObject(MalType.SYMBOL, "nil")


class MalAtom(MalObject):
    """"Mal Atom"""

    def __init__(self, value: MalObject = None):
        super().__init__(MalType.ATOM, value)

    def deref(self) -> MalObject:
        return self._value

    def reset(self, new_value: MalObject) -> None:
        self._value = new_value

    # def swap(self, fn: MalObject, *args: List[MalObject]) -> MalObject:
    #     self._value = mal_apply(fn, self._value, *args)
    #     return self._value
