"""Mal Types"""

from enum import Enum


class MalType(Enum):
    """Mal Type"""

    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    SYMBOL = "SYMBOL"
    LIST = "LIST"
    VECTOR = "VECTOR"
    HASHMAP = "HASHMAP"


class MalObject:
    """Mal Object"""

    def __init__(self, mal_type, value):
        self.mal_type = mal_type
        self.value = value

    def __repr__(self):
        return f"MalObject({self.mal_type}, {self.value})"
