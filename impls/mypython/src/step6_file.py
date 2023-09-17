import sys
import traceback

from mal.core import core_env
from mal.types import MalObject
from mal.eval import mal_eval
from mal.env import Env
from mal.reader import read_str
from mal.printer import pr_str


def mal_read(s: str) -> MalObject:
    return read_str(s)


def mal_print(exp: MalObject) -> str:
    return pr_str(exp, print_readably=True)


def mal_quit():
    sys.exit(0)


def mal_rep(s: str, env: Env) -> str:
    return mal_print(mal_eval(env, mal_read(s)))


def prelude(env: Env):
    mal_rep("(def! not (fn* (a) (if a false true)))", env)
    env["eval"] = lambda ast: mal_eval(env, ast)
    mal_rep("""(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))""", env)


if __name__ == "__main__":
    env = core_env()
    prelude(env)
    while True:
        try:
            line = input("user> ")
            if line == "":
                continue
            print(mal_rep(line, env))
        except EOFError:
            mal_quit()
        except Exception as e:
            print(e)
            print("".join(traceback.format_exception(*sys.exc_info())))
