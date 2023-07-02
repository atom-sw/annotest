# aNNoTest

[![PyPI version](https://badge.fury.io/py/annotest.svg)](https://badge.fury.io/py/annotest)
![GitHub](https://img.shields.io/github/license/atom-sw/annotest)



aNNoTest is a tool (and an approach) to automatically
generating bug-finding inputs for NN program testing.
Paper [An annotation-based approach for finding bugs in
neural network 
programs](https://doi.org/10.1016/j.jss.2023.111669) by
Mohammad Rezaalipour and Carlo A. Furia explains aNNoTest
in details and provides guidelines on how to use it, effectively.


## Installation

Run the following command to install aNNoTest:

```
pip install annotest
```

We have tested aNNoTest on Python 3.6.
But it should work on Python 3.6+ as well.

## Using aNNoTest

aNNoTest is a command line tool.
After annotating your project with 
aN (aNNoTest's annotation language)
you can `cd` to your project directory
and then run aNNoTest.

```
cd path_to_python_project
```

```
annotest
```

Or you can input the project path to aNNoTest:

```
annotest path_to_python_project
```

## Examples

To see examples of using aNNoTest, see
the following repository:

[https://github.com/atom-sw/annotest-subjects](https://github.com/atom-sw/annotest-subjects)


## Citations

[aNNoTest's Journal 
Paper:](https://doi.org/10.1016/j.jss.2023.111669)

```
@article{Rezaalipour:2023,
title = {An annotation-based approach for finding bugs in neural network programs},
journal = {Journal of Systems and Software},
volume = {201},
pages = {111669},
year = {2023},
issn = {0164-1212},
doi = {https://doi.org/10.1016/j.jss.2023.111669},
url = {https://www.sciencedirect.com/science/article/pii/S016412122300064X},
author = {Mohammad Rezaalipour and Carlo A. Furia},
keywords = {Test generation, Neural networks, Debugging, Python}
}
```

# Mirrors

The current repository is a public mirror of
our internal private repository.
We have two public mirrors, which are as follows:

- https://github.com/atom-sw/annotest
- https://github.com/mohrez86/annotest
