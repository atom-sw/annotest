import ast
from typing import List, Optional

import astor

from annotest import file, constant
from annotest.common import string_contains
from annotest.project_info import project_type
from annotest.project_info.decorator_info import decorator_type
from annotest.unittest_engine import astlib
from annotest.unittest_engine.hypothesis_lib import decorator


def _getTestFunctionDecorators(function: project_type.FunctionInfo,
                               enforceDataStrategyArg: bool = False) -> List[ast.Call]:
    astDecoratorList = []

    givenKeywordList = []
    for arg in function.args:
        if arg.type == project_type.ArgType.Arg and not function.argumentIsComplicatedObject(arg.name):
            argumentTypeInformation = function.getArgumentTypeInformationForArgumentName(arg.name)
            argumentDefault = arg.default
            keywordForArg = decorator.getGivenKeywordForArg(arg.name, argumentTypeInformation, argumentDefault)
            # This check is not necessary. Because at this level, functions are all
            # type inferable. But, for now, since not all decorator types are
            # implemented, this check is added so the running examples can be used.
            if keywordForArg is not None:
                givenKeywordList.append(keywordForArg)
    for arg in function.args:
        if arg.type == project_type.ArgType.Vararg and function.argumentHasType(arg.name):
            argumentTypeInformation = function.getArgumentTypeInformationForArgumentName(arg.name)
            keywordForArg = decorator.getGivenKeywordForArg(arg.name, argumentTypeInformation, None)
            # This check is not necessary. Because at this level, functions are all
            # type inferable. But, for now, since not all decorator types are
            # implemented, this check is added so the running examples can be used.
            if keywordForArg is not None:
                givenKeywordList.append(keywordForArg)
    for arg in function.args:
        if arg.type == project_type.ArgType.Kwarg and function.argumentHasType(arg.name):
            argumentTypeInformation = function.getArgumentTypeInformationForArgumentName(arg.name)
            keywordForArg = decorator.getGivenKeywordForArg(arg.name, argumentTypeInformation, None)
            # This check is not necessary. Because at this level, functions are all
            # type inferable. But, for now, since not all decorator types are
            # implemented, this check is added so the running examples can be used.
            if keywordForArg is not None:
                givenKeywordList.append(keywordForArg)

    if function.hasComplicatedArguments() or enforceDataStrategyArg:
        givenKeywordList.append(decorator.getAstKeywordForDataStrategy())

    if len(givenKeywordList) == 0:
        keywordForArg = decorator.getGivenKeywordForNoArgCall()
        givenKeywordList.append(keywordForArg)

    givenDecorator = decorator.getGivenDecorator(givenKeywordList)
    astDecoratorList.append(givenDecorator)

    hasPrecondition = function.hasPreconditionDecorator() or function.needsPreconditionHeathCheck()
    deadlineDecorator = function.getDeadlineDecorator()
    settingsDecorator = decorator.getSettingsDecorator(hasPrecondition, deadlineDecorator)
    astDecoratorList.append(settingsDecorator)

    return astDecoratorList


def _getGeneratorMidArgName(prefix, argName):
    # To handle Python 3.6.
    arg_name = argName
    if isinstance(arg_name, ast.Str):
        arg_name = argName.s

    return prefix + arg_name + "_"


def _getStmtForComplicatedArgument(argTypeInfoDecorator: decorator_type.ArgumentDecorator,
                                   extraPrefix: str = "") -> List[ast.stmt]:
    astStmtList = []
    genFuncInfo: project_type.FunctionInfo = argTypeInfoDecorator.arg_type.generatorFunctionInfo
    midArgNames = []
    argNames = genFuncInfo.getArgNames()
    for item in genFuncInfo.args:
        if item.type == project_type.ArgType.Arg:
            argumentTypeInformation = genFuncInfo.getArgumentTypeInformationForArgumentName(item.name)
            argumentDefault = item.default
            astCallForArg = decorator.getFinalAstCallForArg(argumentTypeInformation, argumentDefault)
            midArgName = _getGeneratorMidArgName(extraPrefix + constant.generatorArgPrefix,
                                                 argTypeInfoDecorator.arg_name) + item.name
            midArgNames.append(midArgName)
            astAssign = astlib.getDrawAssign(midArgName, astCallForArg)
            astStmtList.append(astAssign)

    if genFuncInfo.hasPreconditionDecorator():
        functionPreconditionDecoratorList = genFuncInfo.getPreconditionDecorators()
        for cpItem in functionPreconditionDecoratorList:
            astFunctionPrecondition = astlib.getPreconditionExpr(cpItem.predicate,
                                                                 _getGeneratorMidArgName(extraPrefix +
                                                                                         constant.generatorArgPrefix,
                                                                                         argTypeInfoDecorator.arg_name),
                                                                 argNames)
            astStmtList.append(astFunctionPrecondition)

    current_arg_name = argTypeInfoDecorator.arg_name
    if isinstance(current_arg_name, ast.Str):
        # To handle Python 3.6.
        current_arg_name = argTypeInfoDecorator.arg_name.s

    generatorFunctionCall = astlib.getGeneratorFunctionCall(extraPrefix + current_arg_name,
                                                            genFuncInfo.name,
                                                            midArgNames)
    astStmtList.append(generatorFunctionCall)

    return astStmtList


def _getTestFunctionBody(function: project_type.FunctionInfo,
                         calleeName: str,
                         returnVarName: Optional[str] = None) -> List[ast.stmt]:
    bodyList: List[ast.stmt] = []

    if function.hasComplicatedArguments():
        complicatedArguments = function.getComplicatedArgumentTypeInformationDecorators()
        for item in complicatedArguments:
            currentComplicatedStmtList = _getStmtForComplicatedArgument(item)
            bodyList = bodyList + currentComplicatedStmtList

    if function.hasPreconditionDecorator():
        functionPreconditionDecoratorList = function.getPreconditionDecorators()
        for cpItem in functionPreconditionDecoratorList:
            astFunctionPrecondition = astlib.getPreconditionExpr(cpItem.predicate)
            bodyList.append(astFunctionPrecondition)

    astFunctionCall = astlib.getFunctionCall(function, calleeName, returnVarName)
    bodyList.append(astFunctionCall)

    return bodyList


def _getTestFunctionForFunctionInfo(function: project_type.FunctionInfo) -> ast.FunctionDef:
    astFunctionDef = _getFunctionDefSignature(function)

    astDecoratorList = _getTestFunctionDecorators(function)
    astFunctionDef.decorator_list = astDecoratorList

    astTestFunctionBodyList = _getTestFunctionBody(function, function.name)
    astFunctionDef.body = astTestFunctionBodyList

    return astFunctionDef


def _getFunctionDefSignature(func: project_type.FunctionInfo,
                             functionName: Optional[str] = None,
                             enforceDataStrategyArg: bool = False) -> ast.FunctionDef:
    astFunctionDef = astlib.getEmptyFunctionDefinition("test_" + func.name)
    if functionName is not None:
        astFunctionDef = astlib.getEmptyFunctionDefinition("test_" + functionName)
    astFunctionDef.args.args.append(astlib.getArgFromName("self"))
    for arg in func.args:
        if arg.type == project_type.ArgType.Arg and not func.argumentIsComplicatedObject(arg.name):
            astArg = astlib.getArgFromName(arg.name)
            astFunctionDef.args.args.append(astArg)
    for arg in func.args:
        if arg.type == project_type.ArgType.Vararg and func.argumentHasType(arg.name):
            astArg = astlib.getArgFromName(arg.name)
            astFunctionDef.args.args.append(astArg)
    for arg in func.args:
        if arg.type == project_type.ArgType.Kwarg and func.argumentHasType(arg.name):
            astArg = astlib.getArgFromName(arg.name)
            astFunctionDef.args.args.append(astArg)

    if func.hasComplicatedArguments() or enforceDataStrategyArg:
        astArg = astlib.getArgFromName(constant.dataStrategyArgumentName)
        astFunctionDef.args.args.append(astArg)

    if len(astFunctionDef.args.args) == 1:
        astArg = astlib.getArgFromName(constant.noArgCallParameter)
        astFunctionDef.args.args.append(astArg)

    return astFunctionDef


def _getTestFunctionForConstructor(classInfo: project_type.ClassInfo) -> ast.FunctionDef:
    constructor = classInfo.getConstructor()
    astFunctionDef = _getFunctionDefSignature(constructor, constant.constructorsTestFunctionNamePostfix)
    astDecoratorList = _getTestFunctionDecorators(constructor)
    astFunctionDef.decorator_list = astDecoratorList
    astTestFunctionBodyList = _getTestFunctionBody(constructor, classInfo.name)
    astFunctionDef.body = astTestFunctionBodyList

    return astFunctionDef


def _getConstructorMidArgName(prefix: str, argName: str) -> str:
    return prefix + argName


def _getTestFunctionBodyForImplicitConstructor(classInfo: project_type.ClassInfo) -> List[ast.stmt]:
    stmtList: List[ast.stmt] = []
    constructor = project_type.InstanceMethodInfo(name="__init__", args=[], decorators=[])
    astFunctionCall = astlib.getFunctionCall(constructor, classInfo.name, constant.classObjectInstanceVariableName,
                                             argumentExtraPrefix=constant.constructorArgPrefix)
    stmtList.append(astFunctionCall)

    return stmtList


def _getTestFunctionBodyForConstructorWithDraw(classInfo: project_type.ClassInfo) -> List[ast.stmt]:
    stmtList: List[ast.stmt] = []
    constructor = classInfo.getConstructor()

    for arg in constructor.args:
        if arg.type == project_type.ArgType.Arg and not constructor.argumentIsComplicatedObject(arg.name):
            argumentTypeInformation = constructor.getArgumentTypeInformationForArgumentName(arg.name)
            argumentDefault = arg.default
            astCallForArg = decorator.getFinalAstCallForArg(argumentTypeInformation, argumentDefault)
            midArgName = _getConstructorMidArgName(constant.constructorArgPrefix, arg.name)
            astAssignForArg = astlib.getDrawAssign(midArgName, astCallForArg)
            stmtList.append(astAssignForArg)

    for arg in constructor.args:
        if arg.type == project_type.ArgType.Vararg and constructor.argumentHasType(arg.name):
            argumentTypeInformation = constructor.getArgumentTypeInformationForArgumentName(arg.name)
            astCallForArg = decorator.getFinalAstCallForArg(argumentTypeInformation, None)
            midArgName = _getConstructorMidArgName(constant.constructorArgPrefix, arg.name)
            astAssignForArg = astlib.getDrawAssign(midArgName, astCallForArg)
            stmtList.append(astAssignForArg)

    for arg in constructor.args:
        if arg.type == project_type.ArgType.Kwarg and constructor.argumentHasType(arg.name):
            argumentTypeInformation = constructor.getArgumentTypeInformationForArgumentName(arg.name)
            astCallForArg = decorator.getFinalAstCallForArg(argumentTypeInformation, None)
            midArgName = _getConstructorMidArgName(constant.constructorArgPrefix, arg.name)
            astAssignForArg = astlib.getDrawAssign(midArgName, astCallForArg)
            stmtList.append(astAssignForArg)

    if constructor.hasComplicatedArguments():
        complicatedArguments = constructor.getComplicatedArgumentTypeInformationDecorators()
        for item in complicatedArguments:
            currentComplicatedStmtList = _getStmtForComplicatedArgument(item, constant.constructorArgPrefix)
            stmtList = stmtList + currentComplicatedStmtList

    if constructor.hasPreconditionDecorator():
        functionPreconditionDecoratorList = constructor.getPreconditionDecorators()
        for cpItem in functionPreconditionDecoratorList:
            astFunctionPrecondition = astlib.getPreconditionExpr(cpItem.predicate,
                                                                 constant.constructorArgPrefix,
                                                                 constructor.getArgNames())
            stmtList.append(astFunctionPrecondition)

    astFunctionCall = astlib.getFunctionCall(constructor, classInfo.name, constant.classObjectInstanceVariableName,
                                             argumentExtraPrefix=constant.constructorArgPrefix)
    stmtList.append(astFunctionCall)

    return stmtList


def _getTestFunctionBodyForInstanceMethodCall(instanceMethodInfo: project_type.InstanceMethodInfo) -> List[ast.stmt]:
    astTestFunctionBodyList = _getTestFunctionBody(instanceMethodInfo,
                                                   constant.classObjectInstanceVariableName +
                                                   "." +
                                                   instanceMethodInfo.name)
    return astTestFunctionBodyList


def _getTestFunctionForInstanceMethodNoCcExamples(instanceMethodInfo: project_type.InstanceMethodInfo,
                                                  classInfo: project_type.ClassInfo) -> ast.FunctionDef:
    astFunctionDef = _getFunctionDefSignature(instanceMethodInfo, enforceDataStrategyArg=True)
    astDecoratorList = _getTestFunctionDecorators(instanceMethodInfo, enforceDataStrategyArg=True)
    astFunctionDef.decorator_list = astDecoratorList

    if classInfo.getConstructor() is not None:
        astConstructorInstantiation = _getTestFunctionBodyForConstructorWithDraw(classInfo)
    else:
        astConstructorInstantiation = _getTestFunctionBodyForImplicitConstructor(classInfo)

    astFunctionDef.body = astConstructorInstantiation
    astInstanceMethodCall = _getTestFunctionBodyForInstanceMethodCall(instanceMethodInfo)
    astFunctionDef.body += astInstanceMethodCall
    return astFunctionDef


def _getTestFunctionBodyForConstructorWithExample(classInfo: project_type.ClassInfo,
                                                  currentConstructorExample) -> List[ast.stmt]:
    stmtList: List[ast.stmt] = []
    constructor = classInfo.getConstructor()
    argNameList = []
    for i in range(len(currentConstructorExample.elts)):
        item = currentConstructorExample.elts[i]
        astCallForArg = decorator.getAstCallForJust(item)
        midArgName = _getConstructorMidArgName(constant.constructorArgPrefix, constructor.args[i + 1].name)
        if constructor.args[i + 1].type == project_type.ArgType.Arg:
            argNameList.append(midArgName)
        elif constructor.args[i + 1].type == project_type.ArgType.Vararg:
            argNameList.append("*" + midArgName)
        elif constructor.args[i + 1].type == project_type.ArgType.Kwarg:
            argNameList.append("**" + midArgName)
        astAssignForArg = astlib.getDrawAssign(midArgName, astCallForArg)
        stmtList.append(astAssignForArg)

    astCallForConstructor = astlib.getFunctionCallForArgNames(classInfo.name,
                                                              argNameList,
                                                              constant.classObjectInstanceVariableName)
    stmtList.append(astCallForConstructor)
    return stmtList


def _getTestFunctionForInstanceMethodWithCcExample(instanceMethodInfo: project_type.InstanceMethodInfo,
                                                   classInfo: project_type.ClassInfo,
                                                   currentConstructorExample,
                                                   testFunctionIndex: int) -> ast.FunctionDef:
    currentTestFunctionName = instanceMethodInfo.name + "_" + str(testFunctionIndex)
    astFunctionDef = _getFunctionDefSignature(instanceMethodInfo,
                                              functionName=currentTestFunctionName,
                                              enforceDataStrategyArg=True)
    astDecoratorList = _getTestFunctionDecorators(instanceMethodInfo, enforceDataStrategyArg=True)
    astFunctionDef.decorator_list = astDecoratorList
    astConstructorInstantiation = _getTestFunctionBodyForConstructorWithExample(classInfo, currentConstructorExample)
    astFunctionDef.body = astConstructorInstantiation
    astInstanceMethodCall = _getTestFunctionBodyForInstanceMethodCall(instanceMethodInfo)
    astFunctionDef.body += astInstanceMethodCall

    return astFunctionDef


def _getClassTestClass(classInfo: project_type.ClassInfo) -> [ast.FunctionDef]:
    testFunctionList = []

    if classInfo.getConstructor() is not None:
        astTestFunctionForConstructor = _getTestFunctionForConstructor(classInfo)
        testFunctionList.append(astTestFunctionForConstructor)

    constructorExampleList = classInfo.getConstructorExamples()
    classInstanceMethods = classInfo.getInstanceMethods()
    for instMethod in classInstanceMethods:
        if len(constructorExampleList) == 0:
            astFunctionDef = _getTestFunctionForInstanceMethodNoCcExamples(instMethod, classInfo)
            testFunctionList.append(astFunctionDef)
        else:
            for testFunctionIndex in range(len(constructorExampleList)):
                currentConstructorExample = constructorExampleList[testFunctionIndex]
                astFunctionDef = _getTestFunctionForInstanceMethodWithCcExample(instMethod,
                                                                                classInfo,
                                                                                currentConstructorExample,
                                                                                testFunctionIndex)
                testFunctionList.append(astFunctionDef)

    return testFunctionList


def _generateTestsForModule(module: project_type.ModuleInfo) -> Optional[str]:
    testModuleAst = astlib.getEmptyModule()

    testModuleAst.body += module.get_imports()
    testModuleAst.body.append(astlib.getUnittestImports())
    testModuleAst.body += astlib.getHypothesisImports()
    if module.containsNumpyImportType():
        testModuleAst.body += astlib.getNumpyHypothesisImports()

    testModuleAst.body.append(astlib.getTopLevelItemsImport(module))

    if module.has_module_import_test():
        module_import_test_ast = astlib.get_module_import_test(module)
        testModuleAst.body.append(module_import_test_ast)

    topLevelTestFunctions = []
    for cFunc in module.functions:
        if not cFunc.isExcluded():
            cTestFunction = _getTestFunctionForFunctionInfo(cFunc)
            topLevelTestFunctions.append(cTestFunction)

    if len(topLevelTestFunctions) > 0:
        functionTestClass = astlib.getEmptyUnitTestClass(constant.topLevelFunctionTestClassName)
        functionTestClass.body += topLevelTestFunctions
        testModuleAst.body.append(functionTestClass)

    numberOfTestClasses = 0
    for cClass in module.classes:
        testClassFunctions = _getClassTestClass(cClass)
        if len(testClassFunctions) > 0:
            numberOfTestClasses += 1
            cClassTestClass = astlib.getEmptyUnitTestClass("Test_" + cClass.name)
            cClassTestClass.body = testClassFunctions
            testModuleAst.body.append(cClassTestClass)

    testModuleAst = ast.fix_missing_locations(testModuleAst)
    testModuleAstText = astor.to_source(testModuleAst)

    if len(topLevelTestFunctions) + numberOfTestClasses == 0 and not module.has_module_import_test():
        return None
    else:
        return testModuleAstText


def get_strategy_integer_lists():
    strategy_code = """
from hypothesis.strategies._internal.utils import defines_strategy


@defines_strategy()
def integer_lists_an(min_len=1, max_len=None, min_value=1, max_value=None):
    if max_len is None:
        max_len = min_len + 2
    if max_value is None:
        max_value = min_value + 5
    return st.lists(st.integers(min_value, max_value), min_size=min_len, max_size=max_len)


"""

    return strategy_code


def add_strategy_to_test_module(module_string: str, strategy_name: str):
    module_string_parts = module_string.split("class Test_")
    if strategy_name == constant.ArgumentTypeInformation.IntegerLists.StrategyName:
        strategy_code = get_strategy_integer_lists()
    else:
        raise Exception("Strategy is not supported.")

    new_module_string = module_string_parts[0].strip() + strategy_code
    for index in range(1, len(module_string_parts)):
        new_module_string += "class Test_" + module_string_parts[index].strip()

    return new_module_string


def _module_testing(module: project_type.ModuleInfo):
    moduleString = _generateTestsForModule(module)
    if moduleString is not None:
        if string_contains(moduleString, constant.ArgumentTypeInformation.IntegerLists.StrategyName):
            moduleString = add_strategy_to_test_module(moduleString, constant.ArgumentTypeInformation.IntegerLists.StrategyName)
        testPathOfModule = module.getTestPath()
        file.makeModule(testPathOfModule)
        file.stringToFile(moduleString, testPathOfModule)


def _package_testing(package: project_type.PackageInfo):
    testPath = package.getTestPath()
    file.makePackageSafe(testPath)
    for module in package.modules:
        _module_testing(module)
    for pkg in package.packages:
        _package_testing(pkg)


def generate_tests(projectDat: project_type.ProjectInfo):
    file.makeTestDir()
    for module in projectDat.rootPackage.modules:
        _module_testing(module)
    for pkg in projectDat.rootPackage.packages:
        _package_testing(pkg)
