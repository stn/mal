import sys
import traceback

from mal.types import MalObject, MalType
from mal.eval import mal_eval
from mal.env import Env
from mal.reader import read_str
from mal.printer import pr_str


def mal_read(s: str) -> MalObject:
    return read_str(s)


def mal_print(exp: MalObject) -> str:
    return pr_str(exp)


def mal_quit():
    sys.exit(0)


def mal_rep(s: str, env: Env) -> str:
    return mal_print(mal_eval(env, mal_read(s)))


def create_env() -> Env:
    env = Env()
    env["+"] = lambda a, b: MalObject(MalType.INTEGER, a.value + b.value)
    env["-"] = lambda a, b: MalObject(MalType.INTEGER, a.value - b.value)
    env["*"] = lambda a, b: MalObject(MalType.INTEGER, a.value * b.value)
    env["/"] = lambda a, b: MalObject(MalType.INTEGER, int(a.value / b.value))
    return env


if __name__ == "__main__":
    env = create_env()
    while True:
        try:
            line = input("user> ")
            if line == "":
                continue
            print(mal_rep(line, env))
        except EOFError:
            mal_quit()
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))
