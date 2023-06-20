import ast
import pathlib
from enum import Enum
from typing import List, Optional

from annotest import constant
from annotest.project_info.decorator_info import decorator_type
from annotest.project_info.decorator_info import argument_type
from annotest.project_info.decorator_info.decorator_type import Decorator, ArgumentDecorator


# def _pathToTestPath(path: pathlib.PosixPath) -> pathlib.PosixPath:
#     testPath = constant.testDirPath / path
#     parent = testPath.parent
#     name = "test_" + testPath.name
#     final = parent / name
#     return final

def _pathToTestPath(path: pathlib.PosixPath) -> pathlib.PosixPath:
    parts = list(path.parts)
    for i in range(len(parts)):
        if parts[i].endswith(".py"):
            parts[i] = "test_" + parts[i]
    tmpPath = pathlib.Path(*parts)
    final = constant.testDirPath / tmpPath
    return final


class ArgType(Enum):
    Self = 1
    Arg = 2
    Kwarg = 3
    Vararg = 4


class ArgumentInfo(object):
    def __init__(self,
                 name: str,
                 argType: ArgType,
                 default: ast.expr = None):
        self.name: str = name
        self.type: ArgType = argType
        self.default: ast.expr = default

    def _pretty_representation(self):
        return f"{self.name} - {self.type}"

    def __str__(self):
        return self._pretty_representation()

    def __repr__(self):
        return self._pretty_representation()


class FunctionInfo(object):
    def __init__(self,
                 name: str,
                 args: List[ArgumentInfo],
                 decorators: List[Decorator]):
        self.name: str = name
        self.args: List[ArgumentInfo] = args
        self.decorators: List[Decorator] = decorators

    def _getArgumentDecorators(self) -> List[ArgumentDecorator]:
        argDecoratorList = []
        for decorator in self.decorators:
            if isinstance(decorator, ArgumentDecorator):
                argDecoratorList.append(decorator)
        return argDecoratorList

    def getArgumentTypeInformationForArgumentName(self,
                                                  argName: str) -> Optional[argument_type.ArgumentTypeInformation]:
        argumentDecorators = self._getArgumentDecorators()
        for argumentDecorator in argumentDecorators:

            arg_dec_arg_name = argumentDecorator.arg_name
            if not isinstance(arg_dec_arg_name, str):
                # to handle Python 3.6
                arg_dec_arg_name = arg_dec_arg_name.s

            if arg_dec_arg_name == argName and argumentDecorator.isValid():
                return argumentDecorator.arg_type
        return None

    def argumentHasType(self, argName: str) -> bool:
        argTypeInfo = self.getArgumentTypeInformationForArgumentName(argName)
        if argTypeInfo is not None:
            if isinstance(argTypeInfo, argument_type.ComplicatedObject):
                return argTypeInfo.generatorFunctionInfo is not None and argTypeInfo.generatorFunctionInfo.isTestable()
            else:
                return True
        else:
            return False

    def isTestable(self) -> bool:
        for arg in self.args:
            if arg.type == ArgType.Arg:
                if arg.default is None and not self.argumentHasType(arg.name):
                    return False
        return True

    def getDeadlineDecorator(self) -> Optional[decorator_type.DeadlineDecorator]:
        for decorator in self.decorators:
            if isinstance(decorator, decorator_type.DeadlineDecorator):
                return decorator
        return None

    # def hasDeadlineDecoration(self) -> bool:
    #     deadlineDecorator = self.getDeadlineDecoration()
    #     return deadlineDecorator is not None

    def getPreconditionDecorators(self) -> List[decorator_type.PreconditionDecorator]:
        preconditionDecoratorList = []
        for decorator in self.decorators:
            if isinstance(decorator, decorator_type.PreconditionDecorator):
                preconditionDecoratorList.append(decorator)
        return preconditionDecoratorList

    def hasPreconditionDecorator(self) -> bool:
        preconditionDecorators = self.getPreconditionDecorators()
        return len(preconditionDecorators) > 0

    def getComplicatedArgumentTypeInformationDecorators(self) -> List[decorator_type.ArgumentDecorator]:
        complicatedObjectArgumentTypeInfoList = []
        argumentDecorators = self._getArgumentDecorators()
        for item in argumentDecorators:
            if isinstance(item.arg_type, argument_type.ComplicatedObject):
                complicatedObjectArgumentTypeInfoList.append(item)
        return complicatedObjectArgumentTypeInfoList

    def hasComplicatedArguments(self) -> bool:
        complicatedObjectArgumentTypeInfoList = self.getComplicatedArgumentTypeInformationDecorators()
        return len(complicatedObjectArgumentTypeInfoList) > 0

    def isExcluded(self):
        decorators = self.decorators
        for item in decorators:
            if isinstance(item, decorator_type.ExcludeDecorator):
                return True
        return False

    def argumentIsComplicatedObject(self, argName: str) -> bool:
        complicatedObjectArgumentTypeInfoList = self.getComplicatedArgumentTypeInformationDecorators()

        for item in complicatedObjectArgumentTypeInfoList:

            item_arg_name = item.arg_name
            if isinstance(item_arg_name, ast.Str):
                # To handle Python 3.6.
                item_arg_name = item_arg_name.s

            if item_arg_name == argName:
                return True

        return False

    def isGenerator(self) -> bool:
        for decorator in self.decorators:
            if isinstance(decorator, decorator_type.GeneratorDecorator):
                return True
        return False

    # This method works after the linking phase
    def _hasGeneratorsWithPreconditions(self) -> bool:
        if self.hasComplicatedArguments():
            complicatedObjectArgumentTypeInfoList = self.getComplicatedArgumentTypeInformationDecorators()
            for item in complicatedObjectArgumentTypeInfoList:
                if item.arg_type.generatorFunctionInfo is not None:
                    return item.arg_type.generatorFunctionInfo.hasPreconditionDecorator()
        else:
            return False

    # This method works after the linking phase
    def needsPreconditionHeathCheck(self) -> bool:
        return self.hasPreconditionDecorator() or self._hasGeneratorsWithPreconditions()

    def getArgNames(self, prefix: str = "") -> List[str]:
        argNames = []
        for item in self.args:
            argNames.append(prefix + item.name)

        return argNames


class InstanceMethodInfo(FunctionInfo):
    def __init__(self, name: str,
                 args: List[ArgumentInfo],
                 decorators: List[Decorator]):
        super().__init__(name, args, decorators)

    def isTestable(self) -> bool:
        for arg in self.args:
            if arg.type == ArgType.Arg and arg.name != "self":
                if arg.default is None and not self.argumentHasType(arg.name):
                    return False
        return True


class ClassInfo(object):
    def __init__(self,
                 name: str,
                 instanceMethodsAndConstructor: List[InstanceMethodInfo]):
        self.name = name
        self.instanceMethodsAndConstructor = instanceMethodsAndConstructor

    def getConstructor(self) -> Optional[InstanceMethodInfo]:
        for item in self.instanceMethodsAndConstructor:
            if item.name == "__init__":
                return item
        return None

    def getInstanceMethods(self) -> List[InstanceMethodInfo]:
        instMeths = []
        for item in self.instanceMethodsAndConstructor:
            if item.name != "__init__":
                instMeths.append(item)
        return instMeths

    def _hasTestableInstanceMethod(self) -> bool:
        instMeths = self.getInstanceMethods()
        for item in instMeths:
            if item.isTestable():
                return True
        return False

    def _hasTestableConstructor(self) -> bool:
        constructorMethodInfo = self.getConstructor()
        if constructorMethodInfo is None:
            return True
        else:
            tp = constructorMethodInfo.isTestable()
            return tp

    def isTestable(self) -> bool:
        if self._hasTestableConstructor():
            constructorMethInfo = self.getConstructor()
            if constructorMethInfo is None:
                return True
            else:
                if not constructorMethInfo.isExcluded():
                    return True
                else:
                    return self._hasTestableInstanceMethod()
        else:
            return False

    def _getConstructorExampleDecorator(self) -> Optional[decorator_type.ConstructorExampleDecorator]:
        constructor = self.getConstructor()
        if constructor is None:
            return None
        constructorExampleDecorator = None
        for item in constructor.decorators:
            if isinstance(item, decorator_type.ConstructorExampleDecorator):
                constructorExampleDecorator = item
        return constructorExampleDecorator

    def getConstructorExamples(self) -> List[ast.Tuple]:  # TODO
        constructorExampleDecorator = self._getConstructorExampleDecorator()
        if constructorExampleDecorator is None:
            return []

        constructorExamples = []
        for item in constructorExampleDecorator.elements.elts:
            constructorExamples.append(item)
        return constructorExamples


class ModuleInfo(object):
    def __init__(self,
                 path,
                 functions: List[FunctionInfo],
                 classes: List[ClassInfo],
                 imports: List[ast.stmt],
                 topLevelItemNameList: List[str],
                 has_module_import_test: bool):
        self.path = path
        self.functions: List[FunctionInfo] = functions
        self.classes: List[ClassInfo] = classes
        self.imports: List[ast.stmt] = imports
        self.topLevelItemNameList: List[str] = topLevelItemNameList
        self._has_module_import_test: bool = has_module_import_test

    def getTestPath(self):
        testPath = _pathToTestPath(self.path)
        return testPath

    def containsNumpyImportType(self):
        # TODO: __--__--
        return True

    # For instance if the path to the module is
    # "a/b/c.py",
    # it returns
    # a.b.c
    def getModulePathInImportFormat(self) -> str:
        parts: List[str] = list(self.path.parts)
        tmp = parts[-1]
        parts[-1] = tmp.split(".")[0]
        moduleImportFormat = ".".join(parts)
        return moduleImportFormat

    def getObjectGeneratorFunctions(self) -> List[FunctionInfo]:
        generatorFunctionInfoList = []
        for item in self.functions:
            if item.isGenerator():
                generatorFunctionInfoList.append(item)
        return generatorFunctionInfoList

    def has_module_import_test(self) -> bool:
        return self._has_module_import_test

    def get_imports(self):
        return self.imports


class PackageInfo(object):
    def __init__(self,
                 path: pathlib.PosixPath,
                 modules: List[ModuleInfo],
                 packages,
                 # hasInit: bool
                 ):
        self.path: pathlib.PosixPath = path
        self.modules: List[ModuleInfo] = modules
        self.packages: List[PackageInfo] = packages
        # self.hasInit: bool = hasInit

    def hasPythonModulesInTree(self):
        if len(self.modules) != 0:
            return True
        for pkg in self.packages:
            if pkg.hasPythonModulesInTree():
                return True

        return False

    def hasTestableItem(self):
        if len(self.modules) != 0 or self._hasTestablePackage():
            return True
        return False

    def _hasTestablePackage(self):
        for pg in self.packages:
            if pg.hasTestableItem():
                return True
        return False

    def getTestPath(self):
        testPath = _pathToTestPath(self.path)
        return testPath


class ProjectInfo(object):
    def __init__(self,
                 rootPackage: PackageInfo):
        self.rootPackage = rootPackage
