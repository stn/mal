"""Reader module."""

import re
from typing import List, Optional

from .types import MalObject, MalType, nil, true, false


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


def read_sequence(reader: Reader, start: str, end: str) -> MalObject:
    """Read a sequence."""
    assert next(reader) == start
    ret = []
    token = reader.peek()
    while token != end:
        if token is None:
            raise SyntaxError("unexpected EOF while reading")
        ret.append(read_from(reader))
        token = reader.peek()
    next(reader)
    return ret


def read_list(reader: Reader) -> MalObject:
    """Read a list."""
    return MalObject(MalType.LIST, read_sequence(reader, "(", ")"))


def read_vector(reader: Reader) -> MalObject:
    """Read a vector."""
    return MalObject(MalType.VECTOR, read_sequence(reader, "[", "]"))


def read_hashmap(reader: Reader) -> MalObject:
    """Read a hashmap."""
    return MalObject(MalType.HASHMAP, read_sequence(reader, "{", "}"))


def _unescape(s: str) -> str:
    t = (s.replace(r"\\", "\u029e")
         .replace(r'\"', '"')
         .replace(r"\n", "\n")
         # .replace(r"\t", "\t")
         # .replace(r"\r", "\r")
         # .replace(r"\b", "\b")
         # .replace(r"\f", "\f")
         )
    if t.find("\\") >= 0:
        raise SyntaxError(f"unbalanced \\ \"{s}\"")
    return t.replace("\u029e", "\\")


def read_quote(reader: Reader) -> MalObject:
    """Read quote."""
    assert next(reader) == "'"
    return MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "quote"), read_from(reader)])


def read_deref(reader: Reader) -> MalObject:
    """Read deref."""
    assert next(reader) == "@"
    token = read_atom(reader)
    if token.mal_type != MalType.SYMBOL:
        raise SyntaxError(f"unexpected token: {token} after @")
    return MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "deref"), token])


def read_atom(reader: Reader) -> MalObject:
    """Read an atom."""
    token = next(reader)
    if token[0] == '"':
        if len(token) == 1 or token[-1] != '"':
            raise SyntaxError(f"unexpected EOF while reading. expected '\"', got '{token}'")
        return MalObject(MalType.STRING, _unescape(token[1:-1]))
    if token[0] == ":":
        if len(token) == 1:
            raise SyntaxError(f"unexpected EOF while reading. got '{token}'")
        return MalObject(MalType.KEYWORD, token[1:])
    if NUMBER_PAT.match(token):
        try:
            return MalObject(MalType.INTEGER, int(token))
        except ValueError:
            try:
                return MalObject(MalType.FLOAT, float(token))
            except ValueError:
                raise SyntaxError(f"invalid number: {token}")
    if token == "true":
        return true
    if token == "false":
        return false
    # In mal, nil and false are different.
    if token == "nil":
        return nil
    return MalObject(MalType.SYMBOL, token)


def read_from(reader: Reader):
    """Read from reader."""
    while True:
        token = reader.peek()
        if token == "(":
            return read_list(reader)
        if token == "[":
            return read_vector(reader)
        if token == "{":
            return read_hashmap(reader)
        elif token == ")":
            raise SyntaxError("unbalanced )")
        elif token == "]":
            raise SyntaxError("unbalanced ]")
        elif token == "}":
            raise SyntaxError("unbalanced }")
        elif token == "'":
            return read_quote(reader)
        elif token == "@":
            return read_deref(reader)
        elif token[0] == ";":
            next(reader)
            continue
        else:
            return read_atom(reader)


def read_str(s: str) -> MalObject:
    """Read string."""
    tokens = tokenize(s)
    return read_from(Reader(tokens))
