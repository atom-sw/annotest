# aNNoTest

[![PyPI version](https://badge.fury.io/py/annotest.svg)](https://badge.fury.io/py/annotest)
![GitHub](https://img.shields.io/github/license/atom-sw/annotest)
[![Downloads](https://static.pepy.tech/badge/annotest)](https://pepy.tech/project/annotest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


aNNoTest is a tool (and an approach) to automatically
generate test inputs for neural-network programs written in Python.
The paper [An annotation-based approach for finding bugs in
neural network 
programs](https://doi.org/10.1016/j.jss.2023.111669) by
Mohammad Rezaalipour and Carlo A. Furia presents the aNNoTest approach
and its experimental evaluation; 
this repository describes how to use the tool implementing the approach.


## Installation

aNNoTest is [on PyPI](https://pypi.org/project/annotest/),
so you can install it using `pip`:

```bash
pip install annotest
```

We mainly tested aNNoTest with Python 3.6, but it should also work on later Python versions.


## Using aNNoTest


### Annotations

aNNoTest relies on annotations to generate test inputs.
[Another repository](https://github.com/atom-sw/annotest-subjects)
shows several examples of Python projects annotated with aNNoTest
with different degrees of detail.


### Running aNNoTest

Once a project is annotated, 
run aNNoTest by simply calling `annotest` in the project's root directory `$PROJECT_PATH`:

```bash
cd $PROJECT_PATH
annotest
```

Alternatively, you can supply the project path directly on the command line:

```bash
# in any directory
annotest $PROJECT_PATH
```


## Citing aNNoTest

You can cite the [work on aNNoTest]((https://doi.org/10.1016/j.jss.2023.111669)) as follows:

> Mohammad Rezaalipour, Carlo A. Furia: An annotation-based approach for finding bugs in neural network programs. J. Syst. Softw. 201: 111669 (2023)

```
@article{aNNoTest-JSS,
   title = {An annotation-based approach for finding bugs in neural network programs},
   journal = {Journal of Systems and Software},
   volume = {201},
   pages = {111669},
   year = {2023},
   issn = {0164-1212},
   doi = {https://doi.org/10.1016/j.jss.2023.111669},
   author = {Mohammad Rezaalipour and Carlo A. Furia}
}
```


## Mirrors

This repository is a public mirror of (part of)
aNNoTest's private development repository.
There are two public mirrors, whose content is identical:

- https://github.com/atom-sw/annotest
- https://github.com/mohrez86/annotest
