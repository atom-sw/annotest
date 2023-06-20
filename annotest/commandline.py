import argparse
import pathlib


class CommandLineArgs:
    def __init__(self,
                 projectDirectory: pathlib.PosixPath):
        self._projectDirectory = projectDirectory

    @property
    def projectDirectory(self) -> pathlib.PosixPath:
        return self._projectDirectory


parser = argparse.ArgumentParser(description="generate tests for scientific and ML Python programs.")


def _parserInit():
    parser.add_argument("dir", default=".", nargs="?", metavar="DIR",
                        help="the directory containing the program under tests. If no"
                             " directory is passed, the current directory is selected "
                             "by default.")


def parseArgs() -> CommandLineArgs:
    _parserInit()
    args = parser.parse_args()
    directory = pathlib.Path(args.dir)
    commandLineArgs = CommandLineArgs(directory)
    return commandLineArgs


def printHelpMessage():
    parser.print_help()
