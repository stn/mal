"""Mal Eval"""

from .types import MalObject, MalType, true, false, nil
from .env import Env


def mal_quasiquote(ast: MalObject) -> MalObject:
    """Quasiquote ast."""
    if ast.mal_type == MalType.INTEGER or ast.mal_type == MalType.FLOAT:
        return ast
    # TODO: special object type for true, false, nil
    if ast == nil or ast == false or ast == true:
        return ast
    if ast.mal_type == MalType.LIST:
        if len(ast.value) == 0:
            return ast
        if ast.value[0].value == "unquote":
            if len(ast.value) != 2:
                raise SyntaxError("wrong number of arguments")
            return ast.value[1]
        ret = MalObject(MalType.LIST, [])
        for elem in reversed(ast.value):
            if elem.mal_type == MalType.LIST:
                if len(elem.value) == 0:
                    ret = MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "cons"), elem, ret])
                    continue
                if elem.value[0].value == "splice-unquote":
                    if len(elem.value) != 2:
                        raise SyntaxError("wrong number of arguments")
                    ret = MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "concat"), elem.value[1], ret])
                    continue
            ret = MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "cons"), mal_quasiquote(elem), ret])
        return ret
    if ast.mal_type == MalType.VECTOR:
        # if len(ast.value) == 0:
        #     return ast
        ret = MalObject(MalType.LIST, [])
        for elem in reversed(ast.value):
            if elem.mal_type == MalType.LIST:
                if len(elem.value) == 0:
                    ret = MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "cons"), elem, ret])
                    continue
                if elem.value[0].value == "splice-unquote":
                    if len(elem.value) != 2:
                        raise SyntaxError("wrong number of arguments")
                    ret = MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "concat"), elem.value[1], ret])
                    continue
            ret = MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "cons"), mal_quasiquote(elem), ret])
        return MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "vec"), ret])
    return MalObject(MalType.LIST, [MalObject(MalType.SYMBOL, "quote"), ast])


def eval_ast(env: dict, ast: MalObject) -> MalObject:
    """Evaluate ast with env."""
    if ast.mal_type == MalType.SYMBOL:
        if ast.value in env:
            return env[ast.value]
        raise NameError(f"'{ast.value}' not found")
    elif ast.mal_type == MalType.LIST:
        if len(ast.value) == 0:
            return ast
        return MalObject(MalType.LIST, [mal_eval(env, x) for x in ast.value])
    elif ast.mal_type == MalType.VECTOR:
        if len(ast.value) == 0:
            return ast
        return MalObject(MalType.VECTOR, [mal_eval(env, x) for x in ast.value])
    elif ast.mal_type == MalType.HASHMAP:
        if len(ast.value) == 0:
            return ast
        return MalObject(MalType.HASHMAP, [mal_eval(env, x) for x in ast.value])
    return ast


def mal_apply(func, *args):
    """Apply func to args."""
    if callable(func):
        return func(*args)
    if func.mal_type == MalType.FUNCTION:
        new_env = Env(outer=func.value[0])
        i = 0
        is_rest = False
        for x in func.value[1].value:
            if x.mal_type != MalType.SYMBOL:
                raise SyntaxError(f"{x} is not a symbol")
            if is_rest:
                new_env[x.value] = MalObject(MalType.LIST, list(args[i:]))
                break
            if x.value == "&":
                is_rest = True
                continue
            new_env[x.value] = args[i]
            i += 1
        return mal_eval(new_env, func.value[2])
    raise TypeError(f"{func} is not callable")


def mal_eval(env, exp: MalObject) -> MalObject:
    """Evaluate exp with env."""
    while True:
        exp = mal_macroexpand(env, exp)
        if exp.mal_type != MalType.LIST:
            return eval_ast(env, exp)
        if len(exp.value) == 0:
            return exp
        # Special forms
        if exp.value[0].value == "def!":
            if len(exp.value) != 3:
                raise SyntaxError("wrong number of arguments")
            if exp.value[1].mal_type != MalType.SYMBOL:
                raise SyntaxError("first argument must be a symbol")
            val = mal_eval(env, exp.value[2])
            env[exp.value[1].value] = val
            return val
        if exp.value[0].value == "defmacro!":
            if len(exp.value) != 3:
                raise SyntaxError("wrong number of arguments")
            if exp.value[1].mal_type != MalType.SYMBOL:
                raise SyntaxError("first argument must be a symbol")
            val = mal_eval(env, exp.value[2])
            if val.mal_type != MalType.FUNCTION:
                raise SyntaxError("second argument must be a function")
            macro = MalObject(MalType.FUNCTION, val.value, is_macro_call=True)
            env[exp.value[1].value] = macro
            return nil
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
                new_env[exp.value[1].value[i].value] = mal_eval(new_env, exp.value[1].value[i + 1])
            # TCO
            # original: return mal_eval(new_env, exp.value[2])
            env = new_env
            exp = exp.value[2]
            continue
        if exp.value[0].value == "do":
            if len(exp.value) == 1:
                return nil
            for v in exp.value[1:-1]:
                mal_eval(env, v)
            # TCO
            # original: return mal_eval(env, exp.value[-1])
            exp = exp.value[-1]
            continue
        if exp.value[0].value == "if":
            if len(exp.value) < 3 or len(exp.value) > 4:
                raise SyntaxError("wrong number of arguments")
            condition = mal_eval(env, exp.value[1])
            if condition == false or condition == nil:
                if len(exp.value) == 4:
                    # TCO
                    # original: return mal_eval(env, exp.value[3])
                    exp = exp.value[3]
                    continue
                return nil
            # TCO
            # original: return mal_eval(env, exp.value[2])
            exp = exp.value[2]
            continue
        if exp.value[0].value == "fn*":
            if len(exp.value) != 3:
                raise SyntaxError("wrong number of arguments")
            if exp.value[1].mal_type != MalType.LIST and exp.value[1].mal_type != MalType.VECTOR:
                raise SyntaxError("second argument must be a list or vector")
            new_env = Env(outer=env)
            return MalObject(MalType.FUNCTION, (new_env, exp.value[1], exp.value[2]))
        if exp.value[0].value == "quote":
            if len(exp.value) != 2:
                raise SyntaxError("wrong number of arguments")
            return exp.value[1]
        if exp.value[0].value == "quasiquote":
            if len(exp.value) != 2:
                raise SyntaxError("wrong number of arguments")
            # TCO
            # original: return mal_quasiquote(exp.value[1])
            exp = mal_quasiquote(exp.value[1])
            continue
        if exp.value[0].value == "quasiquoteexpand":
            if len(exp.value) != 2:
                raise SyntaxError("wrong number of arguments")
            return mal_quasiquote(exp.value[1])
        if exp.value[0].value == "macroexpand":
            if len(exp.value) != 2:
                raise SyntaxError("wrong number of arguments")
            return mal_macroexpand(env, exp.value[1])
        # Function call
        evaluated = eval_ast(env, exp)
        func = evaluated.value[0]
        args = evaluated.value[1:]
        # return mal_apply(env, func, *args)
        if callable(func):
            return func(*args)
        if func.mal_type == MalType.FUNCTION:
            new_env = Env(outer=func.value[0])
            i = 0
            is_rest = False
            for x in func.value[1].value:
                if x.mal_type != MalType.SYMBOL:
                    raise SyntaxError(f"{x} is not a symbol")
                if is_rest:
                    new_env[x.value] = MalObject(MalType.LIST, list(args[i:]))
                    break
                if x.value == "&":
                    is_rest = True
                    continue
                new_env[x.value] = args[i]
                i += 1
            # TCO
            # original: return mal_eval(new_env, func.value[2])
            env = new_env
            exp = func.value[2]
            continue
        raise TypeError(f"{func} is not callable")


def is_macro_call(env: Env, ast: MalObject) -> bool:
    if ast.mal_type != MalType.LIST or len(ast.value) == 0 or ast.value[0].mal_type != MalType.SYMBOL:
        return False
    symbol = ast.value[0]
    if symbol.value not in env:
        return False
    func = env[symbol.value]
    if not isinstance(func, MalObject) or func.mal_type != MalType.FUNCTION:
        return False
    return func.is_macro_call


def mal_macroexpand(env: Env, ast: MalObject) -> MalObject:
    """Macroexpand ast with env."""
    while True:
        if not is_macro_call(env, ast):
            return ast
        func = env[ast.value[0].value]
        ast = mal_apply(func, *ast.value[1:])
