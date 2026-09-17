import ast

FORBIDDEN_NODES = (
    ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef,
    ast.For, ast.While, ast.With, ast.Try, ast.Delete,
)

FORBIDDEN_NAMES = {"exec", "eval", "open", "compile", "__import__", "globals", "locals"}


def validate_code(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden operation: {type(node).__name__}")
        if isinstance(node, ast.Name) and (node.id in FORBIDDEN_NAMES or node.id.startswith("__")):
            raise ValueError(f"Forbidden name: {node.id}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise ValueError(f"Forbidden attribute: {node.attr}")


def execute_code(code, df, pd):
    validate_code(code)
    safe_globals = {
        "__builtins__": {"len": len, "min": min, "max": max, "sum": sum, "round": round},
        "df": df.copy(),
        "pd": pd,
    }
    safe_locals = {}
    exec(code, safe_globals, safe_locals)
    if "result" not in safe_locals:
        raise ValueError("Code did not assign result")
    return safe_locals["result"]