import ast
import pathlib
from typing import List, Optional

from annotest import constant
from annotest.project_info.decorator_info.astlib import astToDecorators
from annotest.project_info.project_type import (
    FunctionInfo,
    ClassInfo,
    InstanceMethodInfo,
    ArgumentInfo,
    ArgType,
)


def _astToArguments(arguments: ast.arguments) -> List[ArgumentInfo]:
    argumentsList: List[ArgumentInfo] = []
    numDefaults = len(arguments.defaults)
    numArgs = len(arguments.args)

    for i in range(numArgs - numDefaults):
        name = arguments.args[i].arg
        if name == "self":
            argType = ArgType.Self
        else:
            argType = ArgType.Arg
        ciarg = ArgumentInfo(name, argType)
        argumentsList.append(ciarg)

    tempArgumentsList: List[ArgumentInfo] = []
    for i in range(numDefaults):
        name = arguments.args[0 - i - 1].arg
        if name == "self":
            argType = ArgType.Self
        else:
            argType = ArgType.Arg
        defaultValue = arguments.defaults[0 - i - 1]
        ciarg = ArgumentInfo(name, argType, defaultValue)
        tempArgumentsList.append(ciarg)

    tempArgumentsList.reverse()
    argumentsList = argumentsList + tempArgumentsList

    if arguments.vararg is not None:
        vararg = ArgumentInfo(arguments.vararg.arg, ArgType.Vararg)
        argumentsList.append(vararg)

    if arguments.kwarg is not None:
        kwarg = ArgumentInfo(arguments.kwarg.arg, ArgType.Kwarg)
        argumentsList.append(kwarg)

    return argumentsList


def _astToFunction(func: ast.FunctionDef) -> FunctionInfo:
    # print(ast.dump(func))
    name = func.name
    args = _astToArguments(func.args)
    decorators = astToDecorators(func.decorator_list)
    funcRet = FunctionInfo(name, args, decorators)
    return funcRet


def getModuleFunctions(path: pathlib.PosixPath) -> List[FunctionInfo]:
    functionList: List[FunctionInfo] = []
    with path.open(mode="r") as f:
        tree = ast.parse(f.read())
        # print(ast.dump(tree))
        for item in tree.body:
            if isinstance(item, ast.FunctionDef):
                currentFunction = _astToFunction(item)
                functionList.append(currentFunction)

    # if len(functionList) == 0:
    #     return None
    # else:
    #     return functionList

    return functionList


def has_module_import_test(path: pathlib.Path) -> bool:
    with path.open(mode="r") as f:
        tree = ast.parse(f.read())
        for item in tree.body:
            if (
                isinstance(item, ast.Expr)
                and isinstance(item.value, ast.Call)
                and isinstance(item.value.func, ast.Attribute)
                and item.value.func.attr == constant.module_import_test_annotation
            ):
                return True

        return False


def _isProperty(insMethod) -> bool:
    for item in insMethod.decorator_list:
        if isinstance(item, ast.Name):
            if item.id == "property":
                return True
        # elif isinstance(item, ast.Call):
        #     print("astCall", item.func.attr)


def _isAbstractMethod(insMethod) -> bool:
    for item in insMethod.decorator_list:
        if isinstance(item, ast.Name):
            if item.id == "abstractmethod":
                return True
        # elif isinstance(item, ast.Call):
        #     print("astCall", item.func.attr)


def _astToInstanceMethod(insMethod: ast.FunctionDef) -> Optional[InstanceMethodInfo]:
    if _isProperty(insMethod) or _isAbstractMethod(insMethod):
        return None
    functionInfo1 = _astToFunction(insMethod)
    name = functionInfo1.name
    args = functionInfo1.args
    decorators = functionInfo1.decorators
    instMethodRet = InstanceMethodInfo(name, args, decorators)
    return instMethodRet


def _getInstanceMethods(cls: ast.ClassDef) -> List[InstanceMethodInfo]:
    # print(ast.dump(cls))
    instanceMethodList: List[InstanceMethodInfo] = []
    for item in cls.body:
        if isinstance(item, ast.FunctionDef):
            currentInstanceMethod = _astToInstanceMethod(item)
            if currentInstanceMethod is not None:
                instanceMethodList.append(currentInstanceMethod)

    return instanceMethodList


def _astToClass(cls: ast.ClassDef) -> ClassInfo:
    # print(ast.dump(cls))
    name = cls.name
    instanceMethods = _getInstanceMethods(cls)
    classRet = ClassInfo(name, instanceMethods)
    return classRet


def getModuleClasses(path: pathlib.PosixPath) -> List[ClassInfo]:
    classList: List[ClassInfo] = []
    with path.open(mode="r") as f:
        tree = ast.parse(f.read())
        # print(ast.dump(tree))
        for item in tree.body:
            if isinstance(item, ast.ClassDef):
                class1 = _astToClass(item)
                classList.append(class1)

    # if len(classList) == 0:
    #     return None
    # else:
    #     return classList

    return classList


def getModuleImports(path: pathlib.PosixPath) -> List[ast.stmt]:
    astImportList: List[ast.stmt] = []
    with path.open(mode="r") as f:
        tree = ast.parse(f.read())
        # print(ast.dump(tree))
        for item in tree.body:
            if isinstance(item, ast.Import) or isinstance(item, ast.ImportFrom):
                astImportList.append(item)
    return astImportList


def _get_all_tuple_variable_names(ast_target: ast.Tuple):
    variable_name_set = set()
    for ast_name in ast_target.elts:
        if isinstance(ast_name, ast.Starred):
            variable_name_set.add(ast_name.value.id)
        elif isinstance(ast_name, ast.Tuple):
            all_tuple_var_names = _get_all_tuple_variable_names(ast_name)
            variable_name_set = variable_name_set.union(all_tuple_var_names)
        else:
            variable_name_set.add(ast_name.id)

    return variable_name_set


def _getVariableName(astAssign: ast.Assign) -> List[str]:
    # print(ast.dump(astAssign))
    variableNameSet = set()
    if isinstance(astAssign.targets[0], ast.Name):
        variableNameSet.add(astAssign.targets[0].id)
    elif isinstance(astAssign.targets[0], ast.Tuple):
        all_tuple_var_names = _get_all_tuple_variable_names(astAssign.targets[0])
        variableNameSet = variableNameSet.union(all_tuple_var_names)
    elif isinstance(astAssign.targets[0], ast.Attribute) or isinstance(
        astAssign.targets[0], ast.Subscript
    ):
        # Do not collect attribute setting
        # such as `keras.backend.update = update`
        # or subscript setting such as
        # `os.environ["THEANO_FLAGS"] = "mode=FAST_COMPILE,device=cpu,floatX=float32"`
        # in keras_adversarial_b1
        pass
    else:
        raise Exception("Bug! Incomplete assumptions in variable collection algorithm.")
    return list(variableNameSet)


def getTopLevelItemNameList(path: pathlib.PosixPath) -> List[str]:
    functionNameList = []
    classNameList = []
    globalVariableNameSet = set()
    with path.open(mode="r") as f:
        tree = ast.parse(f.read())
        # print(path)
        # print(ast.dump(tree))
        for item in tree.body:
            if isinstance(item, ast.FunctionDef):
                functionNameList.append(item.name)
            elif isinstance(item, ast.ClassDef):
                classNameList.append(item.name)
            elif isinstance(item, ast.Assign):
                variableNames = _getVariableName(item)
                globalVariableNameSet.update(variableNames)
    topLevelItemsList = classNameList + functionNameList + list(globalVariableNameSet)
    return topLevelItemsList


def moduleHasError(path: pathlib.PosixPath) -> bool:
    try:
        with path.open(mode="r") as f:
            tree = ast.parse(f.read())
    except Exception as exp:
        print(
            f"WARNING: Syntactical error in module `{path}`. No tests were generated for this module."
        )
        # logging.warning(f"Syntactical error in module `{path}`. No tests are generated for this module.")
        # logging.warning(type(exp))
        # logging.warning(exp.args)
        # logging.warning(exp)
        return True
    return False
