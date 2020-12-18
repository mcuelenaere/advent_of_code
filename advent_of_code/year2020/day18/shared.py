import re

from typing import NamedTuple, Tuple, Union


NumberExpr = NamedTuple("NumberExpr", number=int)
OperatorExpr = NamedTuple("OperatorExpr", operator=str)
SubGroupExpr = NamedTuple("SubGroupExpr", expressions=Tuple["Expr"])
Expr = Union[NumberExpr, OperatorExpr, SubGroupExpr]


def parse_expr(text: str) -> Tuple[Expr]:
    text = re.sub(r"\s+", "", text)
    digits = ""
    stack = []
    current_expr = []
    for char in text:
        if char.isdigit():
            digits += char
            continue
        elif len(digits) > 0:
            current_expr.append(NumberExpr(int(digits)))
            digits = ""

        if char in ("+", "*"):
            current_expr.append(OperatorExpr(char))
        elif char == "(":
            stack.append(current_expr)
            current_expr = []
        elif char == ")":
            assert len(stack) > 0
            subgroup = SubGroupExpr(tuple(current_expr))
            current_expr = stack.pop()
            current_expr.append(subgroup)
    assert len(stack) == 0

    if len(digits) > 0:
        current_expr.append(NumberExpr(int(digits)))

    return tuple(current_expr)


def evaluate(expressions: Tuple[Expr]) -> int:
    number = None
    operator = None
    for expr in expressions:
        if isinstance(expr, NumberExpr):
            if number is None:
                number = expr.number
                continue
            else:
                right = expr.number
        elif isinstance(expr, OperatorExpr):
            operator = expr.operator
            continue
        elif isinstance(expr, SubGroupExpr):
            temp = evaluate(expr.expressions)
            if number is None:
                number = temp
                continue
            else:
                right = temp

        assert operator is not None
        if operator == "+":
            number += right
        elif operator == "*":
            number *= right
        operator = None

    return number
