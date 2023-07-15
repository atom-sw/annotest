import pathlib
from typing import Optional

import annotest.project_info.astlib as astlib
from annotest.project_info import generator_linker
from annotest.project_info.project_type import ProjectInfo, PackageInfo, ModuleInfo


def _isInitModule(item):
    rets = item.name == "__init__.py"
    return rets


def _isTestModuleOrPackage(item):
    rets = (
        item.name.startswith("test")
        or item.name.endswith("test")
        or item.name.endswith("tests")
    )
    return rets


def _isValidModule(item):
    rets = item.name.endswith(".py") and not _isTestModuleOrPackage(item)
    # and not _isInitModule(item) \

    return rets


# Test packages and test functions are not collected
def _dirToPackage(directory: pathlib.PosixPath) -> Optional[PackageInfo]:
    moduleList = []
    packageList = []
    # hasInit = False

    for item in directory.iterdir():
        if item.is_dir():
            if not _isTestModuleOrPackage(item):
                p1 = _dirToPackage(item)
                # if p1 is not None:
                packageList.append(p1)
        if item.is_file():
            if _isValidModule(item):
                m1 = _fileToModule(item)
                if m1 is not None:
                    moduleList.append(m1)
            # elif _isInitModule(item):
            #     hasInit = True

    # if len(moduleList) == 0 and len(packageList) == 0:
    #     return None
    # else:
    #     packr = Package(directory, moduleList, packageList, hasInit)
    #     return packr

    # packr = Package(directory, moduleList, packageList, hasInit)
    packr = PackageInfo(directory, moduleList, packageList)
    return packr


def _fileToModule(path: pathlib.PosixPath) -> Optional[ModuleInfo]:
    if astlib.moduleHasError(path):
        return None
    else:
        functions = astlib.getModuleFunctions(path)
        classes = astlib.getModuleClasses(path)
        imports = astlib.getModuleImports(path)
        topLevelItemNameList = astlib.getTopLevelItemNameList(path)
        has_module_import_test = astlib.has_module_import_test(path)
        mr = ModuleInfo(
            path,
            functions,
            classes,
            imports,
            topLevelItemNameList,
            has_module_import_test,
        )
        return mr


def getProject(directory: pathlib.PosixPath) -> ProjectInfo:
    root = _dirToPackage(directory)
    proj1 = ProjectInfo(root)
    generator_linker.linkComplicatedObjectGenerators(proj1)
    return proj1
