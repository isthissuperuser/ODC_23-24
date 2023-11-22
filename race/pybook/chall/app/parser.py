import ast
import logging

l = logging.getLogger('pyb.parser')
l.setLevel(logging.DEBUG)

allowlist = [
    ast.Module,
    # Litterals
    ast.Constant, ast.FormattedValue, ast.JoinedStr, ast.List, ast.Tuple, ast.Set, ast.Dict,
    # Variables
    ast.Name, ast.Load, ast.Store, ast.Del, ast.Starred, 
    # Expressions
    ast.Expr, 
    ast.UnaryOp, ast.UAdd, ast.USub, ast.Not, ast.Invert, 
    ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.MatMult, 
    ast.BoolOp, ast.And, ast.Or, 
    ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
    ast.Call,
    ast.IfExp,
    # Subscripting
    ast.Subscript, ast.Slice,
    # Statements
    ast.Assign, ast.AugAssign, ast.Delete,
    # Control flow
    ast.If, ast.For, ast.While, ast.Break, ast.Continue, 
    ]

def validate_file(filename):
    with open(filename, "r") as f:
        a = ast.parse(f.read())

    for current in ast.walk(a):
        if current.__class__ not in allowlist:
            l.debug("failed, %r", current)
            return False
        if current.__class__ == ast.Call:
            if current.func.__class__  != ast.Name or current.func.id != 'print':
                l.debug("failed call, %r", current.func)
                return False
    return True
