#
#    Copyright (C) Codeplay Software Limited. All Rights Reserved.
#
r"""Code generation package to provide a front-end and tools for producing and
inserting code using the python itertools package.
Full documentation is maintained in documentation.md"""

__version__ = '0.1.0'
__all__ = [
    'generate_source', 'generate_file', 'Itermode', 'Iterable', 'IterGroup',
    'RemovalIterGroup', 'run_all_tests', 'run_func_tests',
    'run_interface_tests', 'run_iter_tests'
]

from .interface import generate_source, generate_file
from .iter_classes import Itermode, Iterable, IterGroup, RemovalIterGroup
from .run_tests import (run_all_tests, run_func_tests, run_interface_tests,
                        run_iter_tests)
