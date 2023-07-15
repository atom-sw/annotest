# Simplification: The ArgumentType obj can only be used as the second
# input of the arg decorator. It cannot be used as a nested
# type inside other ArgumentTypes such as dictionaries.

# Simplification: The ArgumentType obj cannot be used to define
# the type of inputs of generator functions.

# Simplifications: generator functions cannot
# have keyword and non-keyword arguments (e.g., *args and **kwargs).

# Simplification: Generator functions must be defined
# as top level functions inside the modules in which they
# are referred to.

# Simplification: The ArgumentType obj cannot be used
# keyword and non-keyword arguments (e.g., *args and **kwargs)


def integers(min_value=0, max_value=1000):
    """
    :param min_value: Optional[int]
        Default: 0
        Examples: 12
    :param max_value: Optional[int]
        Default: 1000
        Examples: 300
    """
    pass


def floats(
    min_value=None,
    max_value=None,
    allow_nan=None,
    allow_infinity=None,
    width=64,
    exclude_min=False,
    exclude_max=False,
):
    """
    :param min_value: Optional[Union[int, float, Fraction, Decimal]]
    :param max_value: Optional[Union[int, float, Fraction, Decimal]]
    :param allow_nan: Optional[bool]
    :param allow_infinity: Optional[bool]
    :param width: int
    :param exclude_min: bool
    :param exclude_max: bool
    """
    pass


def sampled(elements):
    """
    Used for strings, objects, and callables.
    It can be used for other types as well.
    :param elements: List[Any]
        a list to sample from. The elements can be anything
        but one of our argument types such as
        integers, floats, sampled, and ect.
        Example: [1, 2, 3]
        Example: ["A1", "A2", "A3"]
        Example: [myObject(1), myObject(12), myObject(17)]
    """
    pass


def array_shapes(min_dims=1, max_dims=None, min_side=1, max_side=None):
    """
    Array shapes for numpy arrays.
    :param min_dims: int
    :param max_dims: Optional[int]
    :param min_side: int
    :param max_side: Optional[int]
    """
    pass


def np_arrays(dtype=None, shape=None):
    """
    :param dtype: Optional[numpy.dtype]
        Default: None (all integer and floating dtypes)
        Example: np.dtype("float32")
        Example: np.uint8
    :param shape: Optional[ArgumentType (e.g., samples[...], and array_shapes(...))]
        Default: None (array_shapes with default input values)
        Example: sampled(elements=[(3,), (3,2), (3, 4, 11)])
        Example: array_shapes(min_dims=3)
    """
    pass


def tuples(*args):
    """
    :param args: Several other ArgumentTypes
        Examples: tuples(integers(), floats())
    """
    pass


def dictionaries(keys, values, min_size=0, max_size=None):
    """
    :param keys: ArgumentType
    Type of the keys of the dictionaries
        Example: integers()
        Example: floats()
        Example: sampled(elements=["A", "B"])
    :param values: ArgumentType
    Type of the values of the dictionaries
        Example: integers()
        Example: floats()
        Example: sampled(elements=[1, 2, 3])
    :param min_size: int
        Minimum of the size of the dictionaries
    :param max_size: Optional[int]
        Maximum of the size of the dictionaries
    """
    pass


def obj(generator):
    """
    :param generator: Callable
    Reference to the function, generating instances of the complicated type
        Examples: obj(generator=gen_func01)
    """
    pass


def multiple(*args):
    """
    Used for parameters that can be of more than one type.
    :param args: Several other ArgumentTypes
    Example:
        multiple(integers(), sampled(elements=["A", "B"]))
    """
    return _inner


def integer_lists(min_len=1, max_len=None, min_value=1, max_value=None):
    """
    Used for arguments that are lists of integers.
    :param min_len: int
    :param max_len: int
    :param min_value: int
    :param max_value: int
    """
    pass


def annotest_module_test():
    """
    Modules having this tag will be tested by importing them.
    """
    pass


def _inner(func):
    def wrapper(*arg1, **kwargs1):
        val = func(*arg1, **kwargs1)
        return val

    return wrapper


def precondition(predicate):
    """
    :param predicate: str
        Example:
            @precondition("a > b + 6")
    """
    return _inner


def arg(arg_name, arg_type):
    """
    :param arg_name: str
    :param arg_type: ArgumentType
    """
    return _inner


def deadline(time=None):
    """
    Setting a deadline for each hypothesis examples. if this decoration is not used or no deadline is passed,
    the deadline is 'None', which means each example can run forever.
    :param time: datetime.timedelta.
        Default: None
        Examples:
            from datetime import timedelta
            @deadline(timedelta(seconds=27))
            def function_under_test():
                return None
    """
    return _inner


def exclude():
    return _inner


def generator():
    return _inner


def cc_example(elements):
    """
    Used to provide concrete examples
    of the parameters of a class constructor
    :param elements: List[Tuple]
        Examples:
        @an.cc_example(elements=[(6, 1), (7, 1)])
    """
    return _inner
