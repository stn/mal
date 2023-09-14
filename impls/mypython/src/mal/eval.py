"""Mal Eval"""

from .types import MalObject, MalType


def eval_ast(ast: MalObject, env: dict) -> MalObject:
    """Evaluate ast with env."""
    if ast.mal_type == MalType.SYMBOL:
        value = env.get(ast.value, None)
        if value is None:
            raise NameError(f"'{ast.value}' not found")
        return value
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
        evaluated = eval_ast(exp, env)
        return evaluated.value[0](*evaluated.value[1:])
    return eval_ast(exp, env)
