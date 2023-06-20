import ast
from typing import List, Optional

from annotest import constant
from annotest.project_info.decorator_info import argument_type, decorator_type


def _getAstConstant(value):
    astConstant = ast.Constant(value=value, kind=None)
    return astConstant


def getAstCallForJust(value: ast.expr) -> ast.Call:
    astJust = ast.Call(func=ast.Attribute(value=ast.Name(id='st',
                                                         ctx=ast.Load()), attr='just',
                                          ctx=ast.Load()),
                       args=[value], keywords=[])

    return astJust


def _getAstCallForOneOf(items: List[ast.Call]) -> ast.Call:
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st',
                                                         ctx=ast.Load()),
                                          attr='one_of',
                                          ctx=ast.Load()),
                       args=items,
                       keywords=[])
    return astCall


def getAstKeywordForDataStrategy() -> ast.keyword:
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st',
                                                         ctx=ast.Load()), attr='data',
                                          ctx=ast.Load()),
                       args=[],
                       keywords=[])
    astKeyword = ast.keyword(arg=constant.dataStrategyArgumentName, value=astCall)
    return astKeyword


def _getAstCallForIntegers(argumentTypeInformation: argument_type.Integers) -> ast.Call:
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st', ctx=ast.Load()),
                                          attr='integers', ctx=ast.Load()), args=[],
                       keywords=[ast.keyword(arg='min_value',
                                             value=ast.Constant(value=argumentTypeInformation.min_value, kind=None)),
                                 ast.keyword(arg='max_value',
                                             value=ast.Constant(value=argumentTypeInformation.max_value,
                                                                kind=None))])
    return astCall


def _getAstCallForFloats(argumentTypeInformation: argument_type.Floats) -> ast.Call:
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st', ctx=ast.Load()),
                                          attr='floats', ctx=ast.Load()), args=[],
                       keywords=[ast.keyword(arg='min_value',
                                             value=ast.Constant(value=argumentTypeInformation.min_value, kind=None)),
                                 ast.keyword(arg='max_value',
                                             value=ast.Constant(value=argumentTypeInformation.max_value, kind=None)),
                                 ast.keyword(arg='allow_nan',
                                             value=ast.Constant(value=argumentTypeInformation.allow_nan, kind=None)),
                                 ast.keyword(arg='allow_infinity',
                                             value=ast.Constant(value=argumentTypeInformation.allow_infinity,
                                                                kind=None)),
                                 ast.keyword(arg='width',
                                             value=ast.Constant(value=argumentTypeInformation.width, kind=None)),
                                 ast.keyword(arg='exclude_min',
                                             value=ast.Constant(value=argumentTypeInformation.exclude_min, kind=None)),
                                 ast.keyword(arg='exclude_max',
                                             value=ast.Constant(value=argumentTypeInformation.exclude_max, kind=None))])
    return astCall


def _getAstCallForSampled(argumentTypeInformation: argument_type.Sampled) -> ast.Call:
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st', ctx=ast.Load()),
                                          attr='sampled_from', ctx=ast.Load()),
                       args=[argumentTypeInformation.elements],
                       keywords=[])
    return astCall


def _getAstCallForArrayShapes(argumentTypeInformation: argument_type.ArrayShapes) -> ast.Call:
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='hynp', ctx=ast.Load()),
                                          attr='array_shapes', ctx=ast.Load()),
                       args=[],
                       keywords=[ast.keyword(arg='min_dims',
                                             value=ast.Constant(value=argumentTypeInformation.min_dims, kind=None)),
                                 ast.keyword(arg='max_dims',
                                             value=ast.Constant(value=argumentTypeInformation.max_dims, kind=None)),
                                 ast.keyword(arg='min_side',
                                             value=ast.Constant(value=argumentTypeInformation.min_side, kind=None)),
                                 ast.keyword(arg='max_side',
                                             value=ast.Constant(value=argumentTypeInformation.max_side, kind=None))])
    return astCall


def _getAstCallForNpArrays(argumentTypeInformation: argument_type.NpArrays) -> ast.Call:
    if argumentTypeInformation.dtype is None:
        dtype = ast.Call(func=ast.Attribute(value=ast.Name(id='st', ctx=ast.Load()), attr='one_of', ctx=ast.Load()),
                         args=[ast.Call(func=ast.Attribute(value=ast.Name(id='hynp',
                                                                          ctx=ast.Load()),
                                                           attr='integer_dtypes',
                                                           ctx=ast.Load()),
                                        args=[],
                                        keywords=[]),
                               ast.Call(func=ast.Attribute(value=ast.Name(id='hynp',
                                                                          ctx=ast.Load()),
                                                           attr='floating_dtypes', ctx=ast.Load()),
                                        args=[],
                                        keywords=[])],
                         keywords=[])

    else:
        dtype = argumentTypeInformation.dtype

    if argumentTypeInformation.shape is None:
        defaultArrayShapes = argument_type.ArrayShapes()
        shape = _getAstCallForArrayShapes(defaultArrayShapes)
    else:
        arrayShapes = argumentTypeInformation.shape
        shape = _getAstCallForArgumentTypeInformation(arrayShapes)

    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='hynp', ctx=ast.Load()),
                                          attr='arrays', ctx=ast.Load()), args=[],
                       keywords=[ast.keyword(arg='dtype', value=dtype),
                                 ast.keyword(arg='shape', value=shape)])
    return astCall


def _getAstCallForTuples(argumentTypeInformation: argument_type.Tuples) -> ast.Call:
    argumentTypeAstCallList = []
    for argT in argumentTypeInformation.args:
        cAstCall = _getAstCallForArgumentTypeInformation(argT)
        argumentTypeAstCallList.append(cAstCall)
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st',
                                                         ctx=ast.Load()),
                                          attr='tuples', ctx=ast.Load()),
                       args=argumentTypeAstCallList,
                       keywords=[])
    return astCall


def _getAstCallForDictionaries(argumentTypeInformation: argument_type.Dictionaries) -> ast.Call:
    keysAstCall: ast.Call = _getAstCallForArgumentTypeInformation(argumentTypeInformation.keys)
    valuesAstCall: ast.Call = _getAstCallForArgumentTypeInformation(argumentTypeInformation.values)
    minSizeConstant: ast.Constant = _getAstConstant(argumentTypeInformation.min_size)
    maxSizeConstant: ast.Constant = _getAstConstant(argumentTypeInformation.max_size)

    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st', ctx=ast.Load()), attr='dictionaries', ctx=ast.Load()),
                       args=[],
                       keywords=[ast.keyword(arg='keys', value=keysAstCall),
                                 ast.keyword(arg='values', value=valuesAstCall),
                                 ast.keyword(arg='min_size', value=minSizeConstant),
                                 ast.keyword(arg='max_size', value=maxSizeConstant)])
    return astCall


def _getAstCallForMultipleTypes(argumentTypeInformation: argument_type.MultipleTypes) -> ast.Call:
    argumentTypeAstCallList = []
    for argT in argumentTypeInformation.args:
        cAstCall = _getAstCallForArgumentTypeInformation(argT)
        argumentTypeAstCallList.append(cAstCall)
    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='st', ctx=ast.Load()), attr='one_of', ctx=ast.Load()),
                       args=argumentTypeAstCallList,
                       keywords=[])
    return astCall


def _getAstCallForIntegerLists(argumentTypeInformation: argument_type.IntegerLists) -> ast.Call:
    astCall = ast.Call(func=ast.Name(id=constant.ArgumentTypeInformation.IntegerLists.StrategyName, ctx=ast.Load()), args=[],
                       keywords=[ast.keyword(arg='min_len',
                                             value=ast.Constant(value=argumentTypeInformation.min_len, kind=None)),
                                 ast.keyword(arg='max_len',
                                             value=ast.Constant(value=argumentTypeInformation.max_len, kind=None)),
                                 ast.keyword(arg='min_value',
                                             value=ast.Constant(value=argumentTypeInformation.min_value, kind=None)),
                                 ast.keyword(arg='max_value',
                                             value=ast.Constant(value=argumentTypeInformation.max_value, kind=None))])

    return astCall


def _getAstCallForArgumentTypeInformation(argumentTypeInformation: argument_type.ArgumentTypeInformation) -> ast.Call:
    astCall = None
    if isinstance(argumentTypeInformation, argument_type.Integers):
        astCall = _getAstCallForIntegers(argumentTypeInformation)
    elif isinstance(argumentTypeInformation, argument_type.Floats):
        astCall = _getAstCallForFloats(argumentTypeInformation)
    elif isinstance(argumentTypeInformation, argument_type.Sampled):
        astCall = _getAstCallForSampled(argumentTypeInformation)
    elif isinstance(argumentTypeInformation, argument_type.ArrayShapes):
        astCall = _getAstCallForArrayShapes(argumentTypeInformation)
    elif isinstance(argumentTypeInformation, argument_type.NpArrays):
        astCall = _getAstCallForNpArrays(argumentTypeInformation)
    elif isinstance(argumentTypeInformation, argument_type.Tuples):
        astCall = _getAstCallForTuples(argumentTypeInformation)
    elif isinstance(argumentTypeInformation, argument_type.Dictionaries):
        astCall = _getAstCallForDictionaries(argumentTypeInformation)
    # elif isinstance(argumentTypeInformation, argument_type.ComplicatedObject):
    #     astCall = _getAstCallForDataStrategy()
    elif isinstance(argumentTypeInformation, argument_type.MultipleTypes):
        astCall = _getAstCallForMultipleTypes(argumentTypeInformation)
    elif isinstance(argumentTypeInformation, argument_type.IntegerLists):
        astCall = _getAstCallForIntegerLists(argumentTypeInformation)
    return astCall


def getGivenDecorator(keywords: List[ast.keyword]) -> ast.Call:
    givenDecorator = ast.Call(func=ast.Attribute(value=ast.Name(id='hy',
                                                                ctx=ast.Load()),
                                                 attr='given',
                                                 ctx=ast.Load()),
                              args=[],
                              keywords=keywords)

    return givenDecorator


def getGivenKeywordForNoArgCall() -> ast.keyword:
    astConstant = _getAstConstant(None)
    astJust = getAstCallForJust(astConstant)
    astKeyword = ast.keyword(arg=constant.noArgCallParameter, value=astJust)
    return astKeyword


def getFinalAstCallForArg(argumentTypeInformation: Optional[argument_type.ArgumentTypeInformation],
                          argumentDefault: Optional[ast.expr]) -> ast.Call:
    if argumentDefault is None and argumentTypeInformation is not None:
        astCall = _getAstCallForArgumentTypeInformation(argumentTypeInformation)
    elif argumentDefault is not None and argumentTypeInformation is None:
        astCall = getAstCallForJust(argumentDefault)
    elif argumentDefault is not None and argumentTypeInformation is not None:
        astArgumentInfo = _getAstCallForArgumentTypeInformation(argumentTypeInformation)
        astJust = getAstCallForJust(argumentDefault)
        astCall = _getAstCallForOneOf([astArgumentInfo, astJust])
    else:
        raise Exception("At this point in code, functions must be type inferable.")

    return astCall


def getGivenKeywordForArg(argumentName: str,
                          argumentTypeInformation: Optional[argument_type.ArgumentTypeInformation],
                          argumentDefault: Optional[ast.expr]) -> ast.keyword:
    astCall = getFinalAstCallForArg(argumentTypeInformation, argumentDefault)
    astKeyword = ast.keyword(arg=argumentName, value=astCall)
    return astKeyword


def _getAstKeywordForDeadline(deadlineDecoratorValue: ast.expr) -> ast.keyword:
    astKeyword: ast.keyword = ast.keyword(arg='deadline', value=deadlineDecoratorValue)
    return astKeyword


def _getAstKeywordForHealthCheck() -> ast.keyword:
    astKeyword: ast.keyword = ast.keyword(arg='suppress_health_check', value=ast.List(elts=[ast.Attribute(
        value=ast.Attribute(value=ast.Name(id='hy', ctx=ast.Load()),
                            attr='HealthCheck',
                            ctx=ast.Load()), attr='filter_too_much',
        ctx=ast.Load()),
        ast.Attribute(value=ast.Attribute(value=ast.Name(id='hy',
                                                         ctx=ast.Load()),
                                          attr='HealthCheck',
                                          ctx=ast.Load()),
                      attr='too_slow',
                      ctx=ast.Load())],
        ctx=ast.Load()))
    return astKeyword


def getSettingsDecorator(hasPrecondition: Optional[bool] = None,
                         deadlineDecorator: Optional[decorator_type.DeadlineDecorator] = None) -> ast.Call:
    settingsAstKeywords: List[ast.keyword] = []

    if deadlineDecorator is not None and deadlineDecorator.time is not None:
        astKeywordForDeadline = _getAstKeywordForDeadline(deadlineDecorator.time)
    else:
        astKeywordForDeadline = _getAstKeywordForDeadline(_getAstConstant(None))
    settingsAstKeywords.append(astKeywordForDeadline)

    if hasPrecondition:
        astKeywordForHealthCheck = _getAstKeywordForHealthCheck()
        settingsAstKeywords.append(astKeywordForHealthCheck)

    astCall = ast.Call(func=ast.Attribute(value=ast.Name(id='hy', ctx=ast.Load()),
                                          attr='settings', ctx=ast.Load()),
                       args=[], keywords=settingsAstKeywords)
    return astCall


def getHypothesisDrawAttribute() -> ast.Attribute:
    astAttribute = ast.Attribute(value=ast.Name(id=constant.dataStrategyArgumentName, ctx=ast.Load()), attr='draw',
                                 ctx=ast.Load())
    return astAttribute
