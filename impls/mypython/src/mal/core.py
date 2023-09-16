"""Mal Core"""

from typing import List

from .env import Env
from .types import MalObject, MalType, true, false, nil
from .printer import pr_str


CORE_ENV = Env()

# Special objects
CORE_ENV["true"] = true
CORE_ENV["false"] = false
CORE_ENV["nil"] = nil

# Arithmetic
CORE_ENV["+"] = lambda a, b: MalObject(MalType.INTEGER, a.value + b.value)
CORE_ENV["-"] = lambda a, b: MalObject(MalType.INTEGER, a.value - b.value)
CORE_ENV["*"] = lambda a, b: MalObject(MalType.INTEGER, a.value * b.value)
CORE_ENV["/"] = lambda a, b: MalObject(MalType.INTEGER, int(a.value / b.value))

# List
CORE_ENV["list"] = lambda *args: MalObject(MalType.LIST, list(args))
CORE_ENV["list?"] = lambda a: true if a.mal_type == MalType.LIST else false  # nil is not a list


def mal_empty_p(a: MalObject) -> bool:
    if (a.mal_type == MalType.LIST
            or a.mal_type == MalType.VECTOR
            or a.mal_type == MalType.HASHMAP):
        if len(a.value) == 0:
            return true
    return false


CORE_ENV["empty?"] = mal_empty_p


def mal_count_p(a: MalObject) -> int:
    if a == nil:
        return MalObject(MalType.INTEGER, 0)
    if (a.mal_type == MalType.LIST
            or a.mal_type == MalType.VECTOR):
        return MalObject(MalType.INTEGER, len(a.value))
    if a.mal_type == MalType.HASHMAP:
        return MalObject(MalType.INTEGER, len(a.value) // 2)
    raise TypeError(f"{a} is not a sequence")


CORE_ENV["count"] = mal_count_p


# Comparison
def mal_equal(a: MalObject, b: MalObject) -> bool:
    if a.mal_type == b.mal_type:
        if (a.mal_type == MalType.FLOAT
                or a.mal_type == MalType.FUNCTION
                or a.mal_type == MalType.INTEGER
                or a.mal_type == MalType.KEYWORD
                or a.mal_type == MalType.STRING
                or a.mal_type == MalType.SYMBOL):
            return true if a.value == b.value else false
        if a.mal_type == MalType.HASHMAP and b.mal_type == MalType.HASHMAP:
            if len(a.value) != len(b.value):
                return false
            # TODO: change here when hashmap is implemented correctly
            for x, y in zip(a.value, b.value):
                if not mal_equal(x, y):
                    return false
            return true
    if ((a.mal_type == MalType.LIST or a.mal_type == MalType.VECTOR) and
        (b.mal_type == MalType.LIST or b.mal_type == MalType.VECTOR)):
        if len(a.value) != len(b.value):
            return false
        for x, y in zip(a.value, b.value):
            if not mal_equal(x, y):
                return false
        return true
    return false


def mal_is_less_than(a: MalObject, b: MalObject) -> bool:
    if ((a.mal_type == MalType.FLOAT or a.mal_type == MalType.INTEGER)
            and (b.mal_type == MalType.FLOAT or b.mal_type == MalType.INTEGER)):
        return true if a.value < b.value else false
    raise TypeError(f"{a} and {b} are not comparable")


def mal_is_less_than_or_equal(a: MalObject, b: MalObject) -> bool:
    if ((a.mal_type == MalType.FLOAT or a.mal_type == MalType.INTEGER)
            and (b.mal_type == MalType.FLOAT or b.mal_type == MalType.INTEGER)):
        return true if a.value <= b.value else false
    raise TypeError(f"{a} and {b} are not comparable")


def mal_is_greater_than(a: MalObject, b: MalObject) -> bool:
    if ((a.mal_type == MalType.FLOAT or a.mal_type == MalType.INTEGER)
            and (b.mal_type == MalType.FLOAT or b.mal_type == MalType.INTEGER)):
        return true if a.value > b.value else false
    raise TypeError(f"{a} and {b} are not comparable")


def mal_is_greater_than_or_equal(a: MalObject, b: MalObject) -> bool:
    if ((a.mal_type == MalType.FLOAT or a.mal_type == MalType.INTEGER)
            and (b.mal_type == MalType.FLOAT or b.mal_type == MalType.INTEGER)):
        return true if a.value >= b.value else false
    raise TypeError(f"{a} and {b} are not comparable")


CORE_ENV["="] = mal_equal
CORE_ENV["<"] = mal_is_less_than
CORE_ENV["<="] = mal_is_less_than_or_equal
CORE_ENV[">"] = mal_is_greater_than
CORE_ENV[">="] = mal_is_greater_than_or_equal


def mal_pr_str(*objs: List[MalObject]) -> MalObject:
    """Get string representation of MalObject."""
    return MalObject(MalType.STRING, " ".join([pr_str(obj, print_readably=True) for obj in objs]))


def mal_str(*objs: List[MalObject]) -> MalObject:
    """Get string representation of MalObject."""
    return MalObject(MalType.STRING, "".join([pr_str(obj, print_readably=False) for obj in objs]))


def mal_prn(*objs: List[MalObject]) -> MalObject:
    print(" ".join([pr_str(obj, print_readably=True) for obj in objs]))
    return nil


def mal_println(*objs: List[MalObject]) -> MalObject:
    print(" ".join([pr_str(obj, print_readably=False) for obj in objs]))
    return nil


CORE_ENV["pr-str"] = mal_pr_str
CORE_ENV["str"] = mal_str
CORE_ENV["prn"] = mal_prn
CORE_ENV["println"] = mal_println


def core_env() -> Env:
    return CORE_ENV
