from pathlib import Path

import setuptools

# Load version
root_path = Path(__file__).parent
version_file_path = root_path / "annotest" / "version.py"
__version__ = ""
exec(version_file_path.read_text())
assert __version__ != ""

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aNNoTest",
    version=__version__,
    author="Mohammad Rezaalipour",
    author_email="rezaalipour.mohammad@gmail.com",
    description="A tool to automatically generating bug-finding inputs for neural network program testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atom-sw/annotest",
    packages=setuptools.find_packages(exclude="tests"),
    install_requires=["astor~=0.8.1", "autoflake~=1.4", "hypothesis~=6.4", "black"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["annotest = annotest.__main__:main"]},
)
