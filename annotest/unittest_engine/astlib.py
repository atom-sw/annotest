import ast
from typing import List, Optional

from annotest import constant
from annotest.project_info import project_type


def getEmptyModule() -> ast.Module:
    astModule = ast.Module(body=[], type_ignores=[])
    return astModule


def getUnittestImports() -> ast.stmt:
    astImport = ast.Import(names=[ast.alias(name="unittest", asname=None)])
    return astImport


def getHypothesisImports() -> List[ast.stmt]:
    astImportList = [
        ast.Import(names=[ast.alias(name="hypothesis", asname="hy")]),
        ast.Import(names=[ast.alias(name="hypothesis.strategies", asname="st")]),
    ]
    return astImportList


def getNumpyHypothesisImports() -> List[ast.stmt]:
    astImportList = [
        ast.Import(names=[ast.alias(name="hypothesis.extra.numpy", asname="hynp")]),
        ast.Import(names=[ast.alias(name="numpy", asname="np")]),
    ]
    return astImportList


def getTopLevelItemsImport(module: project_type.ModuleInfo) -> ast.ImportFrom:
    aliasList = []

    for item in module.topLevelItemNameList:
        current = ast.alias(name=item, asname=None)
        aliasList.append(current)

    astImportFrom = ast.ImportFrom(
        module=module.getModulePathInImportFormat(), names=aliasList, level=0
    )

    return astImportFrom


def getEmptyUnitTestClass(className: str) -> ast.ClassDef:
    astClassDef = ast.ClassDef(
        name=className,
        bases=[
            ast.Attribute(
                value=ast.Name(id="unittest", ctx=ast.Load()),
                attr="TestCase",
                ctx=ast.Load(),
            )
        ],
        keywords=[],
        body=[],
        decorator_list=[],
    )

    return astClassDef


def getEmptyFunctionDefinition(funcName: str) -> ast.FunctionDef:
    astFunctionDef = ast.FunctionDef(
        name=funcName,
        args=ast.arguments(
            posonlyargs=[],
            args=[],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=[],
        decorator_list=[],
        returns=None,
        type_comment=None,
    )
    return astFunctionDef


def getArgFromName(argumentName: str) -> ast.arg:
    astArg = ast.arg(arg=argumentName, annotation=None, type_comment=None)
    return astArg


def _getName(name: str) -> ast.Name:
    astName = ast.Name(id=name, ctx=ast.Load())
    return astName


# def getNoReturnFunctionCallForFunctionInfo(function: project_type.FunctionInfo) -> ast.Expr:
#     astCall = ast.Call(func=ast.Name(id=function.name, ctx=ast.Load()),
#                        args=[],
#                        keywords=[])
#     for arg in function.args:
#         if arg.type == project_type.ArgType.Arg:
#             astName = _getName(arg.name)
#             astCall.args.append(astName)
#     for arg in function.args:
#         if arg.type == project_type.ArgType.Vararg and function.argumentHasType(arg.name):
#             astName = _getName("*" + arg.name)
#             astCall.args.append(astName)
#     for arg in function.args:
#         if arg.type == project_type.ArgType.Kwarg and function.argumentHasType(arg.name):
#             astName = _getName("**" + arg.name)
#             astCall.args.append(astName)
#
#     astExpr = ast.Expr(value=astCall)
#     return astExpr


def getPreconditionExpr(
    preconditionString: str,
    variableNamePrefix: str = None,
    variableNames: Optional[List[str]] = None,
) -> ast.Expr:
    if variableNamePrefix is None and variableNames is not None:
        raise Exception()

    if variableNamePrefix is not None and variableNames is None:
        raise Exception()

    def parseString(strCode: str) -> ast.Compare:
        if not isinstance(strCode, str):
            # to handle Python 3.6
            strCode = strCode.s

        parsedCode = ast.parse(strCode)
        return parsedCode.body[0].value

    def contains(name, nameList):
        for item in nameList:
            if item == name:
                return True
        return False

    class VariableNamePrefixAddingVisitor(ast.NodeVisitor):
        def __init__(self, prefix: str, varNames: List[str]):
            self.prefix: str = prefix
            self.varNames = varNames

        def generic_visit(self, node):
            for child in ast.iter_child_nodes(node):
                self.visit(child)
            if isinstance(node, ast.Name):
                if contains(node.id, self.varNames):
                    node.id = self.prefix + node.id
                    ast.NodeVisitor.generic_visit(self, node)

    astPredicate = parseString(preconditionString)
    # print(ast.dump(astPredicate))
    if variableNamePrefix is not None and variableNames is not None:
        prefixVisitor = VariableNamePrefixAddingVisitor(
            variableNamePrefix, variableNames
        )
        prefixVisitor.visit(astPredicate)

    astExpr = ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="hy", ctx=ast.Load()), attr="assume", ctx=ast.Load()
            ),
            args=[astPredicate],
            keywords=[],
        )
    )
    return astExpr


def getDrawAssign(leftName: str, astCallForArg: ast.Call) -> ast.Assign:
    astAssign = ast.Assign(
        targets=[ast.Name(id=leftName, ctx=ast.Store())],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=constant.dataStrategyArgumentName, ctx=ast.Load()),
                attr="draw",
                ctx=ast.Load(),
            ),
            args=[astCallForArg],
            keywords=[],
        ),
        type_comment=None,
    )
    return astAssign


def getGeneratorFunctionCall(
    argNameReturn: str, functionName: str, midArgNames: List[str]
) -> ast.Assign:
    astNameList: List[ast.Name] = []
    for item in midArgNames:
        astName = _getName(item)
        astNameList.append(astName)

    astAssign = ast.Assign(
        targets=[ast.Name(id=argNameReturn, ctx=ast.Store())],
        value=ast.Call(
            func=ast.Name(id=functionName, ctx=ast.Load()),
            args=astNameList,
            keywords=[],
        ),
        type_comment=None,
    )
    return astAssign


# def getClassInstantiation(classInfo: project_type.ClassInfo):
#     argNameList = []
#     constructor = classInfo.getConstructor()
#     for arg in constructor.args:
#         if arg.type == project_type.ArgType.Arg:
#             astName = _getName(arg.name)
#             argNameList.append(astName)
#     for arg in constructor.args:
#         if arg.type == project_type.ArgType.Vararg and constructor.argumentHasType(arg.name):
#             astName = _getName("*" + arg.name)
#             argNameList.append(astName)
#     for arg in constructor.args:
#         if arg.type == project_type.ArgType.Kwarg and constructor.argumentHasType(arg.name):
#             astName = _getName("**" + arg.name)
#             argNameList.append(astName)
#
#     astCall = ast.Call(func=ast.Name(id=classInfo.name, ctx=ast.Load()),
#                        args=argNameList,
#                        keywords=[])
#     astAssign = ast.Assign(targets=[ast.Name(id=constant.classObjectInstanceVariableName, ctx=ast.Store())],
#                            value=astCall,
#                            type_comment=None)
#     return astAssign


# def getFunctionCall(function: project_type.FunctionInfo,
#                     calleeName: str,
#                     returnVarName: Optional[str] = None,
#                     argumentExtraPrefix: str = ""):
#     astCall = ast.Call(func=ast.Name(id=calleeName, ctx=ast.Load()),
#                        args=[],
#                        keywords=[])
#     for arg in function.args:
#         if arg.type == project_type.ArgType.Arg:
#             astName = _getName(argumentExtraPrefix + arg.name)
#             astCall.args.append(astName)
#     for arg in function.args:
#         if arg.type == project_type.ArgType.Vararg and function.argumentHasType(arg.name):
#             astName = _getName("*" + argumentExtraPrefix + arg.name)
#             astCall.args.append(astName)
#     for arg in function.args:
#         if arg.type == project_type.ArgType.Kwarg and function.argumentHasType(arg.name):
#             astName = _getName("**" + argumentExtraPrefix + arg.name)
#             astCall.args.append(astName)
#
#     if returnVarName is None:
#         astStmt = ast.Expr(value=astCall)
#     else:
#         astStmt = ast.Assign(targets=[ast.Name(id=returnVarName, ctx=ast.Store())],
#                              value=astCall,
#                              type_comment=None)
#     return astStmt


def getFunctionCallForArgNames(
    calleeName: str, argNames: List[str], returnVarName: Optional[str] = None
):
    astNameList = []
    for item in argNames:
        astName = _getName(item)
        astNameList.append(astName)

    astCall = ast.Call(
        func=ast.Name(id=calleeName, ctx=ast.Load()), args=astNameList, keywords=[]
    )

    if returnVarName is None:
        astStmt = ast.Expr(value=astCall)
    else:
        astStmt = ast.Assign(
            targets=[ast.Name(id=returnVarName, ctx=ast.Store())],
            value=astCall,
            type_comment=None,
        )
    return astStmt


def getFunctionCall(
    function: project_type.FunctionInfo,
    calleeName: str,
    returnVarName: Optional[str] = None,
    argumentExtraPrefix: str = "",
):
    argNameList: List[str] = []

    for arg in function.args:
        if arg.type == project_type.ArgType.Arg:
            argName = argumentExtraPrefix + arg.name
            argNameList.append(argName)
    for arg in function.args:
        if arg.type == project_type.ArgType.Vararg and function.argumentHasType(
            arg.name
        ):
            argName = "*" + argumentExtraPrefix + arg.name
            argNameList.append(argName)
    for arg in function.args:
        if arg.type == project_type.ArgType.Kwarg and function.argumentHasType(
            arg.name
        ):
            argName = "**" + argumentExtraPrefix + arg.name
            argNameList.append(argName)
    astStmt = getFunctionCallForArgNames(calleeName, argNameList, returnVarName)

    return astStmt


def get_module_import_test(module: project_type.ModuleInfo):
    module_import_format = module.getModulePathInImportFormat()
    ast_module_import = ast.Import(
        names=[ast.alias(name=module_import_format, asname=None)]
    )
    ast_assignment = ast.Assign(
        targets=[ast.Name(id="x", ctx=ast.Store())],
        value=ast.Name(id=module_import_format, ctx=ast.Load()),
    )
    astFunctionDef = getEmptyFunctionDefinition(
        constant.module_import_test_function_name
    )
    astFunctionDef.args.args.append(getArgFromName("self"))
    astFunctionDef.body = [ast_module_import, ast_assignment]
    empty_unit_test_class_ast = getEmptyUnitTestClass(
        constant.module_import_test_class_name
    )
    empty_unit_test_class_ast.body = [astFunctionDef]
    return empty_unit_test_class_ast
