"""Mal Env"""

from typing import Dict

from .types import MalObject


class Env:
    """Mal Environment"""

    def __init__(self, outer: "Env" = None):
        self._data: Dict[str, MalObject] = {}
        self._outer = outer

    def __setitem__(self, key: str, value: MalObject):
        self._data[key] = value

    def __getitem__(self, key: str) -> MalObject:
        if key in self._data:
            return self._data[key]
        if self._outer is not None and key in self._outer:
            return self._outer[key]
        raise NameError(f"'{key}' not found")

    def __contains__(self, key: str) -> bool:
        return (key in self._data) or (self._outer is not None and key in self._outer)
