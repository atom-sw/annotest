import os
import subprocess
import sys

from annotest import commandline, constant

# from annotest.preparation.fixer_step import fixing_process
from annotest.preparation.trimmer import keep_testable_project
from annotest.project_info.collecter import getProject
from annotest.project_info.project_type import ProjectInfo
from annotest.unittest_engine.generator import generate_tests


def remove_unused_imports():
    test_dir_path_str = constant.testDirPath.absolute().resolve()
    command = [
        "autoflake",
        "--remove-all-unused-imports",
        "-i",
        "-r",
        test_dir_path_str,
    ]
    subprocess.run(command)


def blacken_tests():
    test_dir_path_str = constant.testDirPath.absolute().resolve()
    command = ["black", test_dir_path_str]
    subprocess.run(command)


def generate():
    project_dat: ProjectInfo = getProject(constant.projectRoot)
    # fixing_process(project_dat)
    keep_testable_project(project_dat)
    generate_tests(project_dat)
    remove_unused_imports()
    blacken_tests()
    print(f"Test generation finished. Tests are in directory `{constant.testDirPath}`.")


def run():
    command_line_args = commandline.parse_args()
    try:
        os.chdir(command_line_args.project_directory.absolute())
    except FileNotFoundError as err:
        print(err)
        sys.exit()

    generate()
