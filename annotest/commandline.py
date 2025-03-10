import argparse
import pathlib
import sys

from annotest import version


class CommandLineArgs:
    def __init__(self, project_directory: pathlib.Path):
        self._projectDirectory = project_directory

    @property
    def project_directory(self) -> pathlib.Path:
        return self._projectDirectory


parser = argparse.ArgumentParser(
    description="generate tests for scientific and ML Python programs."
)


def _parser_init():
    parser.add_argument(
        "dir",
        default=".",
        nargs="?",
        metavar="DIR",
        help="the directory containing the program under tests. If no"
        " directory is passed, the current directory is selected "
        "by default.",
    )

    parser.add_argument(
        "-v", "--version", action="store_true", help="print version and exit"
    )


def parse_args() -> CommandLineArgs:
    _parser_init()
    args = parser.parse_args()

    if args.version:
        print(f"aNNoTest {version.__version__}")
        sys.exit(0)

    directory = pathlib.Path(args.dir)
    command_line_args = CommandLineArgs(directory)
    return command_line_args
