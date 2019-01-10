#
#    Copyright (C) Codeplay Software Limited. All Rights Reserved.
#
import unittest
from sys import path
import os
from ..internal.funcs import (get_space_count, add_spaces_to_lines, read_from_file,
                          insert_in_source, write_to_file, clang_format)

test_dir = os.path.dirname(os.path.abspath(__file__))

class TestFuncs(unittest.TestCase):
    """Tests each function in the funcs file. Each function is tested
    in a separate method."""

    def test_get_space_count(self):
        s = 'no leading whitespace string'
        s_ws = '    four leading whitespace string'
        self.assertEqual(0, get_space_count(s))
        self.assertEqual(4, get_space_count(s_ws))

    def test_add_spaces_to_lines(self):
        lines = 'a\n  b\nc'
        lines_no_space = add_spaces_to_lines(0, lines)
        lines_1_space = add_spaces_to_lines(1, lines)
        lines_4_space = add_spaces_to_lines(4, lines)
        self.assertEqual('a\n  b\nc', lines_no_space)
        self.assertEqual('a\n   b\n c', lines_1_space)
        self.assertEqual('a\n      b\n    c', lines_4_space)

    def test_read_from_file(self):
        # Generate clean test files
        with open(test_dir + '/testFileEmpty.txt', 'w') as output_file:
            output_file.write('')
        with open(test_dir + '/testFile2Lines.txt', 'w') as output_file:
            output_file.write('a\nb')
        # Perform the test
        empty_file_str = read_from_file(test_dir + '/testFileEmpty.txt')
        two_line_file_str = read_from_file(test_dir + '/testFile2Lines.txt')
        self.assertEqual('', empty_file_str)
        self.assertEqual('a\nb', two_line_file_str)

    def test_insert_in_source(self):
        source = 'a\n  @inP1@\n  c\n@inP2@\ne'
        source2 = insert_in_source(source, '@inP1@', 'b\nb\n  b')
        source3 = insert_in_source(source, '@inP2@', 'd\n  d\nd')
        source4 = insert_in_source(source2, '@inP2@', '  d\n  d\nd')
        self.assertEqual('a\n  @inP1@\n  c\n@inP2@\ne', source)
        self.assertEqual('a\n  b\n  b\n    b\n  c\n@inP2@\ne', source2)
        self.assertEqual('a\n  @inP1@\n  c\nd\n  d\nd\ne', source3)
        self.assertEqual('a\n  b\n  b\n    b\n  c\n  d\n  d\nd\ne', source4)

    def test_write_to_file(self):
        # Generate clean test files
        file_name = test_dir + '/testFileOut.txt'
        with open(file_name, 'w') as output_file:
            output_file.write('')
        # Perform the test
        test_text = 'a b c\nd e f'
        write_to_file(file_name, test_text)
        with open(file_name, 'r') as input_file:
            self.assertEqual(test_text, input_file.read())

    def test_clang_format(self):
        # Generate clean test file
        file_name = test_dir + '/testClangFormat.cpp'
        with open(file_name, 'w') as output_file:
            output_file.write(' int main() { return 0 ; }')
        # Perform the test
        test_text = 'int main() { return 0; }'
        clang_format(file_name, test_dir + '/execute_clang_format.sh')
        with open(file_name, 'r') as input_file:
            self.assertEqual(test_text, input_file.read())


def run_func_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFuncs)
    unittest.TextTestRunner().run(suite)
