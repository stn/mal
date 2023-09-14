"""Mal Types"""

from enum import Enum


class MalType(Enum):
    """Mal Type"""

    FLOAT = "FLOAT"
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
        self.mal_type = mal_type
        self.value = value

    def __repr__(self):
        return f"MalObject({self.mal_type}, {self.value})"


# Special objects
true = MalObject(MalType.SYMBOL, "true")
false = MalObject(MalType.SYMBOL, "false")
nil = MalObject(MalType.SYMBOL, "nil")
