from typing import List

from annotest.project_info.project_type import (
    ProjectInfo,
    PackageInfo,
    FunctionInfo,
    ClassInfo,
)


def _getTestableFunctions(functions: List[FunctionInfo]):
    testableFunctionList = []
    for function in functions:
        if function.isTestable():
            testableFunctionList.append(function)

    return testableFunctionList


def _getTestableInstanceMethodsAndConstructorsOfClass(classInfo: ClassInfo):
    instanceMethodsAndConstructor = []
    constructor = classInfo.getConstructor()

    if constructor is not None:
        instanceMethodsAndConstructor.append(constructor)
    instanceMethods = classInfo.getInstanceMethods()

    for item in instanceMethods:
        if item.isTestable():
            instanceMethodsAndConstructor.append(item)

    return instanceMethodsAndConstructor


def _getTestableClasses(classes: List[ClassInfo]):
    testableClassList = []
    for currentClass in classes:
        if currentClass.isTestable():
            currentClass.instanceMethodsAndConstructor = (
                _getTestableInstanceMethodsAndConstructorsOfClass(currentClass)
            )
            if len(currentClass.instanceMethodsAndConstructor) != 0:
                testableClassList.append(currentClass)

    return testableClassList


def _removeUntestableItemsInPackage(package: PackageInfo):
    for module in package.modules:
        testableFunctions = _getTestableFunctions(module.functions)
        testableClasses = _getTestableClasses(module.classes)
        module.functions = testableFunctions
        module.classes = testableClasses
    for pg in package.packages:
        _removeUntestableItemsInPackage(pg)


def _removeEmptyModules(package: PackageInfo):
    nonEmptyModules = []
    for module in package.modules:
        if (
            len(module.functions) + len(module.classes) != 0
            or module.has_module_import_test()
        ):
            nonEmptyModules.append(module)
    package.modules = nonEmptyModules

    for pg in package.packages:
        _removeEmptyModules(pg)


def _removeEmptyPackages(package: PackageInfo):
    nonEmptyPackages = []
    for pg in package.packages:
        if pg.hasTestableItem():
            nonEmptyPackages.append(pg)
        _removeEmptyPackages(pg)
    package.packages = nonEmptyPackages
    pass


def keepTestableProject(projectDat: ProjectInfo):
    _removeUntestableItemsInPackage(projectDat.rootPackage)
    _removeEmptyModules(projectDat.rootPackage)
    _removeEmptyPackages(projectDat.rootPackage)
