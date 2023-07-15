import ast
from typing import List

from annotest import constant
from annotest.project_info.decorator_info import decorator_type, argument_type


def _astCallToArgumentType(
    astArgumentType: ast.expr,
) -> argument_type.ArgumentTypeInformation:
    args, keywords = _astCallToArgsAndKeywords(
        astArgumentType.args, astArgumentType.keywords
    )

    for i in range(len(args)):
        args[i] = _astExpressionToType(args[i])

    for key, value in keywords.items():
        keywords[key] = _astExpressionToType(value)

    if astArgumentType.func.attr == constant.ArgumentTypeInformation.Integers.Name:
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.Integers.Name)
        argumentType = argument_type.Integers(*args, **keywords)
        return argumentType
    elif astArgumentType.func.attr == constant.ArgumentTypeInformation.Floats.Name:
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.Floats.Name)
        argumentType = argument_type.Floats(*args, **keywords)
        return argumentType
    elif astArgumentType.func.attr == constant.ArgumentTypeInformation.Sampled.Name:
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.Sampled.Name)
        argumentType = argument_type.Sampled(*args, **keywords)
        return argumentType
    elif astArgumentType.func.attr == constant.ArgumentTypeInformation.ArrayShapes.Name:
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.ArrayShapes.Name)
        argumentType = argument_type.ArrayShapes(*args, **keywords)
        return argumentType
    elif astArgumentType.func.attr == constant.ArgumentTypeInformation.NpArrays.Name:
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.NpArray.Name)
        argumentType = argument_type.NpArrays(*args, **keywords)
        return argumentType
    elif astArgumentType.func.attr == constant.ArgumentTypeInformation.Tuples.Name:
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.Tuples.Name)
        if (
            len(keywords) != 0
        ):  # This check is for development purposes and should not exist.
            raise Exception(
                "Something is wrong. How can a function with *args take keyword arguments."
            )
        argumentType = argument_type.Tuples(args)
        return argumentType
    elif (
        astArgumentType.func.attr == constant.ArgumentTypeInformation.Dictionaries.Name
    ):
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.Dictionaries.Name)
        argumentType = argument_type.Dictionaries(*args, **keywords)
        return argumentType
    elif (
        astArgumentType.func.attr
        == constant.ArgumentTypeInformation.ComplicatedObject.Name
    ):
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.ComplicatedObject.Name)
        argumentType = argument_type.ComplicatedObject(*args, **keywords)
        return argumentType
    elif (
        astArgumentType.func.attr == constant.ArgumentTypeInformation.MultipleTypes.Name
    ):
        # print(astArgumentType.func.attr, constant.ArgumentTypeInformation.MultipleTypes.Name)
        if (
            len(keywords) != 0
        ):  # This check is for development purposes and should not exist.
            raise Exception(
                "Something is wrong. How can a function with *args take keyword arguments."
            )
        argumentType = argument_type.MultipleTypes(args)
        return argumentType
    elif (
        astArgumentType.func.attr == constant.ArgumentTypeInformation.IntegerLists.Name
    ):
        argumentType = argument_type.IntegerLists(*args, **keywords)
        return argumentType
    else:
        raise Exception("Argument type not defined.")


def _isArgumentType(astExpression: ast.expr) -> bool:
    if isinstance(astExpression, ast.Call):
        if isinstance(astExpression.func, ast.Attribute):
            if any(astExpression.func.attr == item for item in constant.typeNames):
                return True


def _astExpressionToType(astExpression: ast.expr):
    if _isArgumentType(astExpression):
        value = _astCallToArgumentType(astExpression)
        return value
    elif isinstance(astExpression, ast.Constant):
        return astExpression.value
    else:
        return astExpression


def _astCallToArgsAndKeywords(astArgs: List, astKeywords: List):
    argsList = []
    keywordsDictionary = {}

    for arg in astArgs:
        value = _astExpressionToType(arg)
        argsList.append(value)

    for keyword in astKeywords:
        argName = keyword.arg
        argValue = _astExpressionToType(keyword.value)
        keywordsDictionary[argName] = argValue

    return argsList, keywordsDictionary


def _astToDecorator(astDecorator: ast.Call) -> decorator_type.Decorator:
    args, keywords = _astCallToArgsAndKeywords(astDecorator.args, astDecorator.keywords)

    if astDecorator.func.attr == constant.DecoratorNameInCode.Argument:
        # print(astDecorator.func.attr, constant.DecoratorNameInCode.Argument)
        decorator = decorator_type.ArgumentDecorator(*args, **keywords)
        return decorator
    elif astDecorator.func.attr == constant.DecoratorNameInCode.Deadline:
        # print(astDecorator.func.attr, constant.DecoratorNameInCode.Deadline)
        decorator = decorator_type.DeadlineDecorator(*args, **keywords)
        return decorator
    elif astDecorator.func.attr == constant.DecoratorNameInCode.Exclude:
        # print(astDecorator.func.attr, constant.DecoratorNameInCode.Exclude)
        decorator = decorator_type.ExcludeDecorator()
        return decorator
    elif astDecorator.func.attr == constant.DecoratorNameInCode.Generator:
        # print(astDecorator.func.attr, constant.DecoratorNameInCode.Generator)
        decorator = decorator_type.GeneratorDecorator()
        return decorator
    elif astDecorator.func.attr == constant.DecoratorNameInCode.Precondition:
        # print(astDecorator.func.attr, constant.DecoratorNameInCode.Precondition)
        decorator = decorator_type.PreconditionDecorator(*args, **keywords)
        return decorator
    elif astDecorator.func.attr == constant.DecoratorNameInCode.ConstructorExample:
        # print(astDecorator.func.attr, constant.DecoratorNameInCode.ConstructorExample)
        decorator = decorator_type.ConstructorExampleDecorator(*args, **keywords)
        return decorator


def _listContains(name: str, lst: List[str]):
    for item in lst:
        if name == item:
            return True
    return False


def _isOurDecoration(decorator) -> bool:
    if isinstance(decorator, ast.Call):
        return _listContains(decorator.func.attr, constant.decoratorNames)
    return False


def astToDecorators(astDecorations: List[ast.Call]) -> List[decorator_type.Decorator]:
    decorations: List[decorator_type.Decorator] = []
    for item in astDecorations:
        if _isOurDecoration(item):
            cDec = _astToDecorator(item)
            if cDec is not None:
                decorations.append(cDec)

    return decorations
