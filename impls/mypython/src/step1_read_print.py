import sys
import traceback

from mal.types import MalObject
from mal.reader import read_str
from mal.printer import pr_str


def mal_read(s: str) -> MalObject:
    return read_str(s)


def mal_eval(exp: MalObject) -> MalObject:
    return exp


def mal_print(exp: MalObject) -> str:
    return pr_str(exp)


def mal_quit():
    sys.exit(0)


def mal_rep(s: str) -> str:
    return mal_print(mal_eval(mal_read(s)))


if __name__ == "__main__":
    while True:
        try:
            line = input("user> ")
            if line == "":
                continue
            print(mal_rep(line))
        except EOFError:
            mal_quit()
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))
