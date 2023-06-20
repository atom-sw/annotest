# The each of field of each class in this file must have the same name as the corresponding input of the
# corresponding annotation in the annotation.types
import ast
from typing import List, Optional

from annotest import constant


def to_literal(val):
    # to handle Python 3.6
    lit_val = val
    if isinstance(val, ast.Num):
        lit_val = val.n
    elif isinstance(val, ast.NameConstant):
        lit_val = val.value
    elif isinstance(val, ast.UnaryOp):
        if isinstance(lit_val.op, ast.USub):
            lit_val = -1 * val.operand.n

    return lit_val


class ArgumentTypeInformation(object):
    def pretty_representation(self) -> str:
        return self.__class__.__name__

    def __str__(self):
        return self.pretty_representation()

    def __repr__(self):
        return self.pretty_representation()


class Integers(ArgumentTypeInformation):
    def __init__(self,
                 min_value: int = constant.ArgumentTypeInformation.Integers.min_value,
                 max_value: int = constant.ArgumentTypeInformation.Integers.max_value):
        self.min_value: int = to_literal(min_value)
        self.max_value: int = to_literal(max_value)


class Floats(ArgumentTypeInformation):
    def __init__(self,
                 min_value: float = constant.ArgumentTypeInformation.Floats.min_value,
                 max_value: float = constant.ArgumentTypeInformation.Floats.max_value,
                 allow_nan: bool = constant.ArgumentTypeInformation.Floats.allow_nan,
                 allow_infinity: bool = constant.ArgumentTypeInformation.Floats.allow_infinity,
                 width: int = constant.ArgumentTypeInformation.Floats.width,
                 exclude_min: bool = constant.ArgumentTypeInformation.Floats.exclude_min,
                 exclude_max: bool = constant.ArgumentTypeInformation.Floats.exclude_max):
        self.min_value: float = to_literal(min_value)
        self.max_value: float = to_literal(max_value)
        self.allow_nan: bool = allow_nan
        self.allow_infinity: bool = allow_infinity
        self.width: int = width
        self.exclude_min: bool = to_literal(exclude_min)
        self.exclude_max: bool = to_literal(exclude_max)


class Sampled(ArgumentTypeInformation):
    def __init__(self,
                 elements: ast.expr):
        self.elements: ast.expr = elements


class ArrayShapes(ArgumentTypeInformation):
    def __init__(self,
                 min_dims=constant.ArgumentTypeInformation.ArrayShapes.min_dims,
                 max_dims=constant.ArgumentTypeInformation.ArrayShapes.max_dims,
                 min_side=constant.ArgumentTypeInformation.ArrayShapes.min_side,
                 max_side=constant.ArgumentTypeInformation.ArrayShapes.max_side):
        self.min_dims = to_literal(min_dims)
        self.max_dims = to_literal(max_dims)
        self.min_side = to_literal(min_side)
        self.max_side = to_literal(max_side)


class NpArrays(ArgumentTypeInformation):
    def __init__(self,
                 dtype: Optional[ast.expr] = constant.ArgumentTypeInformation.NpArrays.dtype,
                 shape: Optional[ArgumentTypeInformation] = constant.ArgumentTypeInformation.NpArrays.shape):
        self.dtype: Optional[ast.expr] = dtype
        self.shape: Optional[ArgumentTypeInformation] = shape


class Tuples(ArgumentTypeInformation):
    def __init__(self,
                 args: List[ArgumentTypeInformation]):
        self.args = args


class Dictionaries(ArgumentTypeInformation):
    def __init__(self,
                 keys: ArgumentTypeInformation,
                 values: ArgumentTypeInformation,
                 min_size=constant.ArgumentTypeInformation.Dictionaries.min_size,
                 max_size=constant.ArgumentTypeInformation.Dictionaries.max_size):
        self.keys: ArgumentTypeInformation = keys
        self.values: ArgumentTypeInformation = values
        self.min_size = constant.ArgumentTypeInformation.Dictionaries.min_size = min_size
        self.max_size = constant.ArgumentTypeInformation.Dictionaries.max_size = max_size


class ComplicatedObject(ArgumentTypeInformation):
    def __init__(self,
                 generator: ast.expr):
        self.generator: ast.expr = generator
        self.generatorFunctionInfo = None

    def setGeneratorFunctionInfo(self, generatorFunctionInfo):
        self.generatorFunctionInfo = generatorFunctionInfo

    def getGeneratorName(self) -> str:
        return self.generator.id


class MultipleTypes(ArgumentTypeInformation):
    def __init__(self,
                 args: List[ArgumentTypeInformation]):
        self.args = args


class IntegerLists(ArgumentTypeInformation):
    def __init__(self,
                 min_len=constant.ArgumentTypeInformation.IntegerLists.min_len,
                 max_len=constant.ArgumentTypeInformation.IntegerLists.max_len,
                 min_value=constant.ArgumentTypeInformation.IntegerLists.min_value,
                 max_value=constant.ArgumentTypeInformation.IntegerLists.max_value):
        self.min_len: int = to_literal(min_len)
        self.max_len: int = to_literal(max_len)
        self.min_value: int = to_literal(min_value)
        self.max_value: int = to_literal(max_value)
