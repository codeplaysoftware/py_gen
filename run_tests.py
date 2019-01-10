#
#    Copyright (C) Codeplay Software Limited. All Rights Reserved.
#
from .testing.test_funcs import run_func_tests as run_func_tests_internal
from .testing.test_interface import run_interface_tests as run_interface_tests_internal
from .testing.test_iters import run_iter_tests as run_iter_tests_internal
import os

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
