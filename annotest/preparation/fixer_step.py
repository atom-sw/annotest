from annotest import file
from annotest.project_info.project_type import ProjectInfo, PackageInfo


def _addMissingInitFiles(package: PackageInfo):
    if package.hasPythonModulesInTree():
        file.makeEmptyInitFileSafe(package.path)
    for pkg in package.packages:
        _addMissingInitFiles(pkg)


def fixing_process(projectDat: ProjectInfo):
    _addMissingInitFiles(projectDat.rootPackage)
