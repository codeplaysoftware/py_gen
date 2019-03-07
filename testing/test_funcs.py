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

import unittest
import os
from ..internal.funcs import (get_space_count, add_spaces_to_lines,
                              read_from_file, insert_in_source, write_to_file,
                              clang_format)

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


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
        with open(TEST_DIR + '/testFileEmpty.txt', 'w') as output_file:
            output_file.write('')
        with open(TEST_DIR + '/testFile2Lines.txt', 'w') as output_file:
            output_file.write('a\nb')
        # Perform the test
        empty_file_str = read_from_file(TEST_DIR + '/testFileEmpty.txt')
        two_line_file_str = read_from_file(TEST_DIR + '/testFile2Lines.txt')
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
        file_name = TEST_DIR + '/testFileOut.txt'
        with open(file_name, 'w') as output_file:
            output_file.write('')
        # Perform the test
        test_text = 'a b c\nd e f'
        write_to_file(file_name, test_text)
        with open(file_name, 'r') as input_file:
            self.assertEqual(test_text, input_file.read())

    def test_clang_format(self):
        # Generate clean test file
        file_name = TEST_DIR + '/testClangFormat.cpp'
        with open(file_name, 'w') as output_file:
            output_file.write(' int main() { return 0 ; }')
        # Perform the test
        test_text = 'int main() { return 0; }'
        clang_format(file_name, TEST_DIR + '/execute_clang_format.sh')
        with open(file_name, 'r') as input_file:
            self.assertEqual(test_text, input_file.read())


def run_func_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFuncs)
    unittest.TextTestRunner().run(suite)
