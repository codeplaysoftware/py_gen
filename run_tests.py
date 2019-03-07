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

from .testing.test_funcs import run_func_tests as run_func_tests_internal
from .testing.test_interface import run_interface_tests as run_interface_tests_internal
from .testing.test_iters import run_iter_tests as run_iter_tests_internal


def run_all_tests():
    run_func_tests()
    run_interface_tests()
    run_iter_tests_internal()


def run_func_tests():
    run_func_tests_internal()


def run_interface_tests():
    run_interface_tests_internal()


def run_iter_tests():
    run_iter_tests_internal()
