import sys

from mal.types import MalObject
from mal.reader import read_str
from mal.printer import pr_str


def mal_read() -> MalObject:
    line = input("user> ")
    return read_str(line)


def mal_eval(exp: MalObject) -> MalObject:
    return exp


def mal_print(exp: MalObject) -> str:
    print(pr_str(exp))


def mal_quit():
    sys.exit(0)


if __name__ == "__main__":
    while True:
        s = ""
        try:
            s = mal_read()
        except EOFError:
            mal_quit()
        ret = mal_eval(s)
        mal_print(ret)
