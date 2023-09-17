"""Mal Printer"""

from .types import MalObject, MalType


def _escape(s: str) -> str:
    """Escape string."""
    return s.replace("\\", r"\\").replace('"', r'\"').replace("\n", r"\n")


def pr_str(mal_object: MalObject, print_readably: bool = True) -> str:
    """Print string representation of MalObject."""
    if mal_object.mal_type == MalType.STRING:
        if print_readably:
            return f'"{_escape(mal_object.value)}"'
        return mal_object.value
    elif mal_object.mal_type == MalType.KEYWORD:
        return f":{mal_object.value}"
    elif mal_object.mal_type == MalType.LIST:
        return f"({' '.join([pr_str(x, print_readably=print_readably) for x in mal_object.value])})"
    elif mal_object.mal_type == MalType.VECTOR:
        return f"[{' '.join([pr_str(x, print_readably=print_readably) for x in mal_object.value])}]"
    elif mal_object.mal_type == MalType.HASHMAP:
        return f"{{{' '.join([pr_str(x, print_readably=print_readably) for x in mal_object.value])}}}"
    elif mal_object.mal_type == MalType.FUNCTION:
        return f"<function {mal_object.value}>"
    elif mal_object.mal_type == MalType.ATOM:
        return f"(atom {pr_str(mal_object.value, print_readably=print_readably)})"
    return str(mal_object.value)
