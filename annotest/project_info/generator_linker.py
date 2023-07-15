# In this version, we assume a generator function is defined
# inside the module in which the decorator using it exists.
from typing import List, Optional

from annotest.project_info import project_type
from annotest.project_info.decorator_info import decorator_type


def _getFunctionInfoByName(
    functionName: str, functionInfoList: List[project_type.FunctionInfo]
) -> Optional[project_type.FunctionInfo]:
    for item in functionInfoList:
        if item.name == functionName:
            return item
    return None


def _linkInFunction(
    functionInfo: project_type.FunctionInfo,
    generatorFunctionsList: List[project_type.FunctionInfo],
):
    complicatedArgTypeDecoratorList = (
        functionInfo.getComplicatedArgumentTypeInformationDecorators()
    )
    for item in complicatedArgTypeDecoratorList:
        generatorName = item.arg_type.getGeneratorName()
        cFunctionInfo = _getFunctionInfoByName(generatorName, generatorFunctionsList)
        item.arg_type.setGeneratorFunctionInfo(cFunctionInfo)


def _linkInModule(moduleInfo: project_type.ModuleInfo):
    generatorFunctionsList = moduleInfo.getObjectGeneratorFunctions()

    # Linking top level functions
    for item in moduleInfo.functions:
        if item.hasComplicatedArguments():
            _linkInFunction(item, generatorFunctionsList)

    # Linking instance methods in classes
    for cls in moduleInfo.classes:
        for instMet in cls.instanceMethodsAndConstructor:
            if instMet.hasComplicatedArguments():
                _linkInFunction(instMet, generatorFunctionsList)


def _linkInPackage(packageInfo: project_type.PackageInfo):
    for item in packageInfo.modules:
        _linkInModule(item)

    for item in packageInfo.packages:
        _linkInPackage(item)


def linkComplicatedObjectGenerators(projectInfo: project_type.ProjectInfo):
    root = projectInfo.rootPackage
    _linkInPackage(root)
