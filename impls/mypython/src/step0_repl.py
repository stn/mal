import sys


def mal_read(s: str) -> str:
    return s


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
            s = input("user> ")
        except EOFError:
            mal_quit()
        s = mal_read(s)
        ret = mal_eval(s)
        mal_print(ret)
