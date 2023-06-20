# The each of field of each class in this file must have the same name as the corresponding input of the
# corresponding annotation in the annotation.types
import ast
from typing import Optional

from annotest.project_info.decorator_info.argument_type import ArgumentTypeInformation


class Decorator(object):
    pass


class ArgumentDecorator(Decorator):
    def __init__(self,
                 arg_name: str,
                 arg_type: ArgumentTypeInformation):
        self.arg_name: str = arg_name
        self.arg_type: ArgumentTypeInformation = arg_type

    def pretty_representation(self) -> str:
        return str(self.arg_type)

    def __str__(self):
        return self.pretty_representation()

    def __repr__(self):
        return self.pretty_representation()

    def isValid(self):
        if isinstance(self.arg_type, ArgumentTypeInformation):
            return True
        return False


class PreconditionDecorator(Decorator):
    def __init__(self,
                 predicate: str):
        self.predicate: str = predicate


class DeadlineDecorator(Decorator):
    def __init__(self,
                 time: Optional[ast.expr] = None):
        self.time: Optional[ast.expr] = time


class ExcludeDecorator(Decorator):
    pass


class GeneratorDecorator(Decorator):
    pass


class ConstructorExampleDecorator(Decorator):
    def __init__(self,
                 elements: ast.expr):
        self.elements: ast.expr = elements
