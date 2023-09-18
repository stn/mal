"""Mal Core"""

from typing import List, Union

from .env import Env
from .eval import mal_apply
from .types import MalAtom, MalObject, MalType, true, false, nil
from .printer import pr_str
from .reader import read_str


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


def mal_empty_p(a: MalObject) -> bool:
    if (a.mal_type == MalType.LIST
            or a.mal_type == MalType.VECTOR
            or a.mal_type == MalType.HASHMAP):
        if len(a.value) == 0:
            return true
    return false


def mal_count_p(a: MalObject) -> int:
    if a == nil:
        return MalObject(MalType.INTEGER, 0)
    if (a.mal_type == MalType.LIST
            or a.mal_type == MalType.VECTOR):
        return MalObject(MalType.INTEGER, len(a.value))
    if a.mal_type == MalType.HASHMAP:
        return MalObject(MalType.INTEGER, len(a.value) // 2)
    raise TypeError(f"{a} is not a sequence")


def mal_cons(a: MalObject, b: MalObject) -> MalObject:
    if b == nil:
        return MalObject(MalType.LIST, [a])
    if b.mal_type == MalType.LIST or b.mal_type == MalType.VECTOR:
        return MalObject(MalType.LIST, [a] + b.value)
    # if b.mal_type == MalType.VECTOR:
    #     return MalObject(MalType.VECTOR, [a] + b.value)
    raise TypeError(f"{b} is not a sequence")


def mal_concat(*args: List[MalObject]) -> MalObject:
    lst = []
    for arg in args:
        if arg.mal_type == MalType.LIST or arg.mal_type == MalType.VECTOR:
            lst += arg.value
        else:
            raise TypeError(f"{arg} is not a sequence")
    return MalObject(MalType.LIST, lst)


def mal_vec(a: MalObject) -> MalObject:
    if a.mal_type == MalType.LIST:
        return MalObject(MalType.VECTOR, a.value)
    if a.mal_type == MalType.VECTOR:
        return a
    raise TypeError(f"{a} is not a sequence")


CORE_ENV["list"] = lambda *args: MalObject(MalType.LIST, list(args))
CORE_ENV["list?"] = lambda a: true if a.mal_type == MalType.LIST else false  # nil is not a list
CORE_ENV["empty?"] = mal_empty_p
CORE_ENV["count"] = mal_count_p
CORE_ENV["cons"] = mal_cons
CORE_ENV["concat"] = mal_concat
CORE_ENV["vec"] = mal_vec


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


# Reader
def mal_read_str(s: Union[str, MalObject]) -> MalObject:
    """Read string."""
    if isinstance(s, MalObject):
        return read_str(s.value)
    return read_str(s)


def mal_slurp(filename: Union[str, MalObject]) -> MalObject:
    """Read file."""
    if isinstance(filename, MalObject):
        filename = filename.value
    with open(filename, "r") as f:
        return MalObject(MalType.STRING, f.read())


CORE_ENV["read-string"] = mal_read_str
CORE_ENV["slurp"] = mal_slurp


# Atom

def mal_atom(x: MalObject) -> MalObject:
    """Create atom."""
    return MalAtom(x)


def mal_reset(a: MalAtom, new_value: MalObject) -> MalObject:
    """Reset atom."""
    a.reset(new_value)
    return a.deref()


def mal_swap(a: MalAtom, fn: MalObject, *args: List[MalObject]) -> MalObject:
    """Swap atom with the given fn result."""
    a.reset(mal_apply(fn, a.deref(), *args))
    return a.deref()


CORE_ENV["atom"] = mal_atom
CORE_ENV["atom?"] = lambda a: true if a.mal_type == MalType.ATOM else false
CORE_ENV["deref"] = lambda a: a.deref()
CORE_ENV["reset!"] = mal_reset
CORE_ENV["swap!"] = mal_swap


def core_env() -> Env:
    return CORE_ENV
