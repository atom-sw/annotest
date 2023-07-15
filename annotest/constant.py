import pathlib


projectRoot: pathlib.PosixPath = pathlib.Path(".")
testDirName: str = "test_annotest"
testDirPath: pathlib.PosixPath = projectRoot / testDirName


# Name of decorators in SUT
class DecoratorNameInCode(object):
    Argument = "arg"
    Deadline = "deadline"
    Exclude = "exclude"
    Generator = "generator"
    Precondition = "precondition"
    ConstructorExample = "cc_example"


decoratorNames = [
    DecoratorNameInCode.Argument,
    DecoratorNameInCode.Deadline,
    DecoratorNameInCode.Exclude,
    DecoratorNameInCode.Generator,
    DecoratorNameInCode.Precondition,
    DecoratorNameInCode.ConstructorExample,
]


# Name of argument types and their defaults in SUT
class ArgumentTypeInformation(object):
    class Integers(object):
        Name = "integers"
        min_value = 0
        max_value = 1000

    class Floats(object):
        Name = "floats"
        min_value = None
        max_value = None
        allow_nan = None
        allow_infinity = None
        width = 64
        exclude_min = False
        exclude_max = False

    class Sampled(object):
        Name = "sampled"

    class ArrayShapes(object):
        Name = "array_shapes"
        min_dims = 1
        max_dims = None
        min_side = 1
        max_side = None

    class NpArrays(object):
        Name = "np_arrays"
        dtype = None
        shape = None

    class Tuples(object):
        Name = "tuples"

    class Dictionaries(object):
        Name = "dictionaries"
        min_size = 0
        max_size = None

    class ComplicatedObject(object):
        Name = "obj"

    class MultipleTypes(object):
        Name = "multiple"

    class IntegerLists(object):
        Name = "integer_lists"
        StrategyName = "integer_lists_an"
        min_len = 1
        max_len = None
        min_value = 1
        max_value = None


typeNames = [
    ArgumentTypeInformation.Integers.Name,
    ArgumentTypeInformation.Floats.Name,
    ArgumentTypeInformation.Sampled.Name,
    ArgumentTypeInformation.ArrayShapes.Name,
    ArgumentTypeInformation.NpArrays.Name,
    ArgumentTypeInformation.Tuples.Name,
    ArgumentTypeInformation.Dictionaries.Name,
    ArgumentTypeInformation.ComplicatedObject.Name,
    ArgumentTypeInformation.MultipleTypes.Name,
    ArgumentTypeInformation.IntegerLists.Name,
]

topLevelFunctionTestClassName = "Test_TopLevelFunctions"
noArgCallParameter = "noArgCall"
dataStrategyArgumentName = "st_for_data"
generatorArgPrefix = "co_"
classObjectInstanceVariableName = "obj"
constructorsTestFunctionNamePostfix = "init"
constructorArgPrefix = "cc_"

module_import_test_annotation = "annotest_module_test"
module_import_test_class_name = "test_ImportModule"
module_import_test_function_name = "test_import_module"
