import sys


def mal_read(prompt="user> ") -> str:
    return input(prompt)


def mal_eval(exp: str) -> str:
    return exp


def mal_print(exp: str) -> str:
    print(exp)


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
