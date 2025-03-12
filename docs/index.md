# aNNoTest Documentation

[![PyPI version](https://badge.fury.io/py/annotest.svg)](https://badge.fury.io/py/annotest)
![GitHub](https://img.shields.io/github/license/atom-sw/annotest)
[![Downloads](https://static.pepy.tech/badge/annotest)](https://pepy.tech/project/annotest)
[![Docs](https://readthedocs.org/projects/annotest/badge/?version=latest)](https://annotest.readthedocs.io/en/latest/)
![Research](https://img.shields.io/badge/Research-Driven-lightgrey)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](https://github.com/atom-sw/annotest)

aNNoTest is a tool (and an approach) to automatically
generate test inputs for neural-network programs written in Python.
The paper [An annotation-based approach for finding bugs in
neural network 
programs](https://doi.org/10.1016/j.jss.2023.111669) by
Mohammad Rezaalipour and Carlo A. Furia presents the aNNoTest approach
and its experimental evaluation.


## Installation

aNNoTest is [on PyPI](https://pypi.org/project/annotest/),
so you can install it using `pip`:

```bash
pip install annotest
```

To install the latest (unreleased) version, use the following command:

```bash
pip install git+https://github.com/atom-sw/annotest
```

We mainly tested aNNoTest with Python 3.6, but it should also work on later Python versions.


## Using aNNoTest


### Annotations

aNNoTest relies on annotations to generate test inputs.
[This repository](https://github.com/atom-sw/annotest-subjects)
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


## Publications on aNNoTest

- Mohammad Rezaalipour and Carlo A. Furia. 
**aNNoTest: An Annotation-based Test Generation Tool for Neural Network Programs.**
In Proceedings of the 39th IEEE International Conference on Software Maintenance and Evolution (ICSME — tool demo track).
Pgg. 574–579, IEEE Computer Society, October 2023.
[https://doi.org/10.1109/ICSME58846.2023.00075](https://doi.org/10.1109/ICSME58846.2023.00075)

```
@InProceedings{RF-ICSME23-tool-annotest,
  author = {Mohammad Rezaalipour and Carlo A. Furia},
  title = {{aNNoTest}: An Annotation-based Test Generation Tool for Neural Network Programs},
  booktitle = {Proceedings of the 39th IEEE International Conference on Software Maintenance and Evolution (ICSME)},
  pages = {574--579},
  year = {2023},
  month = {October},
  doi = {https://doi.org/10.1109/ICSME58846.2023.00075},
}
```

- Mohammad Rezaalipour and Carlo A. Furia.
**An Annotation-based Approach for Finding Bugs in Neural Network Programs.**
Journal of Systems and Software, 201:111669.
Elsevier, July 2023.
[https://doi.org/10.1016/j.jss.2023.111669](https://doi.org/10.1016/j.jss.2023.111669)

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
