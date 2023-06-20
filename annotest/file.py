import os
import pathlib
import shutil

from annotest import constant
from annotest.project_info.project_type import ProjectInfo, PackageInfo


def makeDirSafe(path: pathlib.PosixPath):
    if not path.exists():
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)


def removeDir(dir: pathlib.PosixPath):
    if dir.exists():
        shutil.rmtree(dir)


def makeEmptyInitFileSafe(parentDir: pathlib.PosixPath):
    path = parentDir / '__init__.py'
    if not path.exists():
        try:
            f = open(path, 'w+')
            f.close()
        except OSError:
            print("Creation of the file %s failed" % path)


def makePackageSafe(path):
    makeDirSafe(path)
    makeEmptyInitFileSafe(path)


def makeTestDir():
    # removeDir(constant.testDirPath)
    makePackageSafe(constant.testDirPath)


def makeModule(path: pathlib.PosixPath):
    try:
        f = open(path, 'w+')
        f.close()
    except OSError:
        print("Creation of the file %s failed" % path)


def stringToFile(text: str, path: pathlib.PosixPath):
    if path.exists():
        with open(path, "w") as file:
            file.write(text)
