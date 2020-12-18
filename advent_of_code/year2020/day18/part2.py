from typing import Tuple

from .shared import Expr, OperatorExpr, SubGroupExpr, evaluate, parse_expr


def mangle(expressions: Tuple[Expr]) -> Tuple[Expr]:
    expressions = list(
        SubGroupExpr(mangle(expr.expressions)) if isinstance(expr, SubGroupExpr) else expr for expr in expressions
    )

    # wrap expressions with an `+` operator in a subgroup
    indices = tuple(i for i, expr in enumerate(expressions) if isinstance(expr, OperatorExpr) and expr.operator == "+")
    for i in reversed(indices):
        expressions[i - 1 : i + 2] = [SubGroupExpr(tuple(expressions[i - 1 : i + 2]))]

    return tuple(expressions)


def calculate(text: str) -> int:
    total = 0
    for line in text.splitlines():
        total += evaluate(mangle(parse_expr(line)))
    return total


assert calculate("1 + 2 * 3 + 4 * 5 + 6") == 231
assert calculate("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert calculate("2 * 3 + (4 * 5)") == 46
assert calculate("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert calculate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert calculate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
