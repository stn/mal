"""Mal Printer"""

from .types import MalObject, MalType


def pr_str(mal_object: MalObject):
    """Print string representation of MalObject."""
    if mal_object.mal_type == MalType.LIST:
        return f"({' '.join([pr_str(x) for x in mal_object.value])})"
    return str(mal_object.value)
