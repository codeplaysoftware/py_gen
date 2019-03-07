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
from string import Template
import os
import sys
from ..interface import generate_source, generate_file
from ..iter_classes import Itermode, Iterable, IterGroup, RemovalIterGroup

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestInterface(unittest.TestCase):
    """Tests each function in the interface file. Each function is tested
    in a separate method."""

    def test_generate_source(self):
        source = 'Line one\n  @ip1@\n    @ip2@\nEnding line'
        iter_groups = [
            IterGroup('@ip1@', Template('a ${key0}\n  ${key1}\nb'), [
                Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2),
                Iterable('key1', ['d', 'e'], Itermode.combinationsWR, 3)
            ]),
            IterGroup('@ip2@', Template('    1 ${key2}${key3}\n'), [
                Iterable('key2', ['1 2', '3'], Itermode.permutations, 2),
                Iterable('key3', ['xyzw'], Itermode.product, 3)
            ])
        ]
        returned_str = generate_source(source, iter_groups)
        self.assertEqual(
            'Line one\n  a ab\n    ddd\n  ba ac\n    ddd\n  ba bc\
\n    ddd\n  ba ab\n    dde\n  ba ac\n    dde\n  ba bc\n    dde\n  ba ab\n    d\
ee\n  ba ac\n    dee\n  ba bc\n    dee\n  ba ab\n    eee\n  ba ac\n    eee\n  \
ba bc\n    eee\n  b\n        1 1 23xyzwxyzwxyzw\n        1 31 2xyzwxyzwxyzw\n\n\
Ending line', returned_str)

    def test_generate_source_comb_iter(self):
        source = '@ip1@'
        iter_groups = [
            IterGroup(
                '@ip1@',
                Template('${key0}  ${key1}  |\n'), [
                    Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2,
                             True),
                    Iterable('key1', ['3', '2', '1'], Itermode.combinations, 2)
                ],
                combine_iters=True)
        ]
        returned_str = generate_source(source, iter_groups)
        self.assertEqual('a, b  32  |\na, c  31  |\nb, c  21  |\n',
                         returned_str)

    def test_generate_source_removal_iter(self):
        source = '@ip1@'
        iter_groups = [
            RemovalIterGroup('@ip1@', Template('${key0}  ${key1}  |\n'), [
                Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2,
                         True),
                Iterable('key1', ['3', '2', '1'], Itermode.combinations, 2)
            ], [
                Iterable('key0', ['a', 'b'], Itermode.combinations, 2, True),
                Iterable('key1', ['3', '2'], Itermode.combinations, 2)
            ])
        ]
        returned_str = generate_source(source, iter_groups)
        self.assertEqual(
            'a, c  31  |\nb, c  31  |\na, c  21  |\nb, c  21  |\n',
            returned_str)

    def test_generate_source_comb_removal_iter(self):
        source = '@ip1@'
        iter_groups = [
            RemovalIterGroup(
                '@ip1@',
                Template('${key0}  ${key1}  |\n'), [
                    Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2,
                             True),
                    Iterable('key1', ['3', '2', '1'], Itermode.combinations, 2)
                ], [
                    Iterable('key0', ['a', 'b'], Itermode.combinations, 2,
                             True),
                    Iterable('key1', ['3', '2'], Itermode.combinations, 2)
                ],
                combine_iters=True)
        ]
        returned_str = generate_source(source, iter_groups)
        self.assertEqual('a, c  31  |\nb, c  21  |\n', returned_str)

    def test_generate_file(self):
        # Test variables
        file_name = TEST_DIR + '/testFileGenerate.txt'
        iter_groups = [
            IterGroup('@ip1@', Template('a ${key0} c ${key1} e\n'), [
                Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2),
                Iterable('key1', ['a', 'b'], Itermode.product, 2)
            ]),
            IterGroup('@ip2@', Template('1 ${key0} 2\n'), [
                Iterable('key0', ['1', '2', '3'], Itermode.combinationsWR, 3)
            ])
        ]
        # Clean the test file first
        with open(file_name + '.in', 'w') as output_file:
            output_file.write('Line one\n  @ip1@\n    @ip2@\nEnding line')
        # Do the test
        returned_str = generate_file(
            file_name + '.in', file_name, iter_groups, format_generated=False)
        self.assertEqual(
            'Line one\n  a ab c aa e\n  a ac c aa e\n  a bc c aa e\
\n  a ab c ab e\n  a ac c ab e\n  a bc c ab e\n  a ab c ba e\n  a ac c ba e\n  \
a bc c ba e\n  a ab c bb e\n  a ac c bb e\n  a bc c bb e\n\n    1 111 2\n    1 \
112 2\n    1 113 2\n    1 122 2\n    1 123 2\n    1 133 2\n    1 222 2\n    1 2\
23 2\n    1 233 2\n    1 333 2\n\nEnding line', returned_str)

    @unittest.skipIf(
        sys.platform.startswith("win"),
        "formatting tests are disabled on Windows")
    def test_generate_formatted_file(self):
        # Test variables
        file_name = TEST_DIR + '/testFormattedFileGenerate.txt'
        iter_group = [
            IterGroup(
                '@ip1@',
                Template('int ${var} ${op} 0;\n'), [
                    Iterable('var', ['a', 'b', 'c'], Itermode.combinations, 1),
                    Iterable('op', ['=', '=', '='], Itermode.combinations, 1)
                ],
                combine_iters=True)
        ]
        # Clean the test file first
        unformatted_input = 'int main() {\n@ip1@\n\n\nreturn 0;}\n'
        with open(file_name + '.in', 'w') as output_file:
            output_file.write(unformatted_input)
        # Perform the test
        generate_file(
            file_name + '.in',
            file_name,
            iter_group,
            format_generated=True,
            format_script=TEST_DIR + '/execute_clang_format.sh')
        # Note: We do not test for an exact input, as different clang format
        # versions and configurations could exist for different users. The best
        # we can do is test 'some' formatting happened.
        with open(file_name, 'r') as input_file:
            self.assertNotEqual(unformatted_input, input_file.read())


def run_interface_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInterface)
    unittest.TextTestRunner().run(suite)
