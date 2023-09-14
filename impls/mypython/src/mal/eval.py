"""Mal Eval"""

from .types import MalObject, MalType
from .env import Env


def eval_ast(ast: MalObject, env: dict) -> MalObject:
    """Evaluate ast with env."""
    if ast.mal_type == MalType.SYMBOL:
        if ast.value in env:
            return env[ast.value]
        raise NameError(f"'{ast.value}' not found")
    elif ast.mal_type == MalType.LIST:
        if len(ast.value) == 0:
            return ast
        return MalObject(MalType.LIST, [mal_eval(x, env) for x in ast.value])
    elif ast.mal_type == MalType.VECTOR:
        if len(ast.value) == 0:
            return ast
        return MalObject(MalType.VECTOR, [mal_eval(x, env) for x in ast.value])
    elif ast.mal_type == MalType.HASHMAP:
        if len(ast.value) == 0:
            return ast
        return MalObject(MalType.HASHMAP, [mal_eval(x, env) for x in ast.value])
    return ast


def mal_eval(exp: MalObject, env) -> MalObject:
    """Evaluate exp with env."""
    if exp.mal_type == MalType.LIST:
        if len(exp.value) == 0:
            return exp
        # Special forms
        if exp.value[0].value == "def!":
            if len(exp.value) != 3:
                raise SyntaxError("wrong number of arguments")
            if exp.value[1].mal_type != MalType.SYMBOL:
                raise SyntaxError("first argument must be a symbol")
            val = mal_eval(exp.value[2], env)
            env[exp.value[1].value] = val
            return val
        if exp.value[0].value == "let*":
            if len(exp.value) != 3:
                raise SyntaxError("wrong number of arguments")
            if exp.value[1].mal_type != MalType.LIST and exp.value[1].mal_type != MalType.VECTOR:
                raise SyntaxError("second argument must be a list or vector")
            if len(exp.value[1].value) % 2 != 0:
                raise SyntaxError("odd number of forms in binding vector")
            new_env = Env(outer=env)
            for i in range(0, len(exp.value[1].value), 2):
                if exp.value[1].value[i].mal_type != MalType.SYMBOL:
                    raise SyntaxError("binding form must be a symbol")
                new_env[exp.value[1].value[i].value] = mal_eval(exp.value[1].value[i + 1], new_env)
            return mal_eval(exp.value[2], new_env)
        # Function call
        evaluated = eval_ast(exp, env)
        return evaluated.value[0](*evaluated.value[1:])
    return eval_ast(exp, env)
