"""Reader module."""

import re
from typing import List, Optional

from .types import MalObject, MalType


TOKEN_PAT = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""")
NUMBER_PAT = re.compile(r"""^-?([0-9]+(\.[0-9]+)?|(\.[0-9]+))$""")


class Reader:
    """Reader class."""

    def __init__(self, tokens: List[str]):
        """Initialize reader."""
        self.tokens = tokens
        self.position = 0

    def __enter__(self):
        """Enter context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context."""
        pass

    def __iter__(self):
        """Iterate over tokens."""
        return self

    def __next__(self):
        """Get next token."""
        if self.position >= len(self.tokens):
            raise StopIteration
        token = self.tokens[self.position]
        self.position += 1
        return token

    def peek(self) -> Optional[str]:
        """Peek at next token."""
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]


def tokenize(s: str) -> List[str]:
    """Tokenize string."""
    return re.findall(TOKEN_PAT, s)


def read_list(reader: Reader) -> MalObject:
    """Read list."""
    assert next(reader) == "("
    ret = []
    token = reader.peek()
    while token != ")":
        if token is None:
            raise SyntaxError("unexpected EOF while reading")
        ret.append(read_from(reader))
        token = reader.peek()
    next(reader)
    return MalObject(MalType.LIST, ret)


def read_atom(reader: Reader) -> MalObject:
    """Read atom."""
    token = next(reader)
    if token.startswith('"'):
        # TODO: unescape the string
        return MalObject(MalType.STRING, token[1:-1])
    if NUMBER_PAT.match(token):
        try:
            return MalObject(MalType.INTEGER, int(token))
        except ValueError:
            try:
                return MalObject(MalType.FLOAT, float(token))
            except ValueError:
                raise SyntaxError(f"invalid number: {token}")
    return MalObject(MalType.SYMBOL, token)


def read_from(reader: Reader):
    """Read from reader."""
    while True:
        token = reader.peek()
        if token == "(":
            return read_list(reader)
        elif token == ")":
            raise SyntaxError("unexpected )")
        elif token[0] == ";":
            next(reader)
            continue
        else:
            return read_atom(reader)


def read_str(s: str):
    """Read string."""
    tokens = tokenize(s)
    return read_from(Reader(tokens))
