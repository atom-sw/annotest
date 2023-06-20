import ast

from annotest.project_info.decorator_info.argument_type import to_literal


def test_to_literal_ast_num():
    val_in = 5
    val = ast.Num(col_offset=60, n=val_in)
    lit_val = to_literal(val)
    assert lit_val == val_in


def test_to_literal_ast_name_constant():
    val_in = True
    val = ast.NameConstant(value=val_in)
    lit_val = to_literal(val)
    assert lit_val == val_in


def test_to_literal_ast_unary_op():
    val_in = 3
    val = ast.UnaryOp(op=ast.USub(),
                      operand=ast.Num(n=3))
    lit_val = to_literal(val)
    assert lit_val == -1 * val_in
