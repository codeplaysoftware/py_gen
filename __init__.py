#   Copyright (C) Codeplay Software Limited.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use these files except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   For your convenience, a copy of the License has been included in this
#   repository.
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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
