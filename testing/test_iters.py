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
from ..internal.iters import (
    gen_combinations, gen_combinations_with_replacement, gen_permutations,
    gen_product, dispatch_iterations, gen_combinations_list,
    gen_combinations_with_replacement_list, gen_permutations_list,
    gen_product_list, combined_dispatcher, removal_dispatcher,
    combined_removal_dispatcher)
from ..iter_classes import Iterable, Itermode


class TestIters(unittest.TestCase):
    """Tests each function in the iters file. Each function is tested
    in a separate method."""

    def test_1_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(key='id', vals=['b'], itermode=Itermode.combinations)
        res = gen_combinations(t, it)
        self.assertEqual(res.template, 'a b c | ')

    def test_1_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['b'],
            itermode=Itermode.combinations,
            iter_modifier=2)
        res = gen_combinations(t, it)
        self.assertEqual(res.template, '')

    def test_2_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id', vals=['a', 'b'], itermode=Itermode.combinations)
        res = gen_combinations(t, it)
        self.assertEqual(res.template, 'a a c | a b c | ')

    def test_2_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b'],
            itermode=Itermode.combinations,
            iter_modifier=2)
        res = gen_combinations(t, it)
        self.assertEqual(res.template, 'a ab c | ')

    def test_3_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b', 'c'],
            itermode=Itermode.combinations,
            iter_modifier=2)
        res = gen_combinations(t, it)
        self.assertEqual(res.template, 'a ab c | a ac c | a bc c | ')


class TestGenCombinationsWR(unittest.TestCase):
    def test_1_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(key='id', vals=['b'], itermode=Itermode.combinationsWR)
        res = gen_combinations_with_replacement(t, it)
        self.assertEqual(res.template, 'a b c | ')

    def test_1_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['b'],
            itermode=Itermode.combinationsWR,
            iter_modifier=2)
        res = gen_combinations_with_replacement(t, it)
        self.assertEqual(res.template, 'a bb c | ')

    def test_2_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id', vals=['a', 'b'], itermode=Itermode.combinationsWR)
        res = gen_combinations_with_replacement(t, it)
        self.assertEqual(res.template, 'a a c | a b c | ')

    def test_2_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b'],
            itermode=Itermode.combinationsWR,
            iter_modifier=2)
        res = gen_combinations_with_replacement(t, it)
        self.assertEqual(res.template, 'a aa c | a ab c | a bb c | ')

    def test_3_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b', 'c'],
            itermode=Itermode.combinationsWR,
            iter_modifier=2)
        res = gen_combinations_with_replacement(t, it)
        self.assertEqual(
            res.template,
            'a aa c | a ab c | a ac c | a bb c | a bc c | a cc c | ')


class TestGenPermutations(unittest.TestCase):
    def test_1_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(key='id', vals=['b'], itermode=Itermode.permutations)
        res = gen_permutations(t, it)
        self.assertEqual(res.template, 'a b c | ')

    def test_1_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['b'],
            itermode=Itermode.permutations,
            iter_modifier=2)
        res = gen_permutations(t, it)
        self.assertEqual(res.template, '')

    def test_2_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id', vals=['a', 'b'], itermode=Itermode.permutations)
        res = gen_permutations(t, it)
        self.assertEqual(res.template, 'a a c | a b c | ')

    def test_2_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b'],
            itermode=Itermode.permutations,
            iter_modifier=2)
        res = gen_permutations(t, it)
        self.assertEqual(res.template, 'a ab c | a ba c | ')

    def test_3_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b', 'c'],
            itermode=Itermode.permutations,
            iter_modifier=2)
        res = gen_permutations(t, it)
        self.assertEqual(
            res.template,
            'a ab c | a ac c | a ba c | a bc c | a ca c | a cb c | ')


class TestGenProduct(unittest.TestCase):
    def test_1_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(key='id', vals=['b'], itermode=Itermode.product)
        res = gen_product(t, it)
        self.assertEqual(res.template, 'a b c | ')

    def test_1_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id', vals=['b'], itermode=Itermode.product, iter_modifier=2)
        res = gen_product(t, it)
        self.assertEqual(res.template, 'a bb c | ')

    def test_2_value_mod_1(self):
        t = Template('a ${id} c | ')
        it = Iterable(key='id', vals=['a', 'b'], itermode=Itermode.product)
        res = gen_product(t, it)
        self.assertEqual(res.template, 'a a c | a b c | ')

    def test_2_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b'],
            itermode=Itermode.product,
            iter_modifier=2)
        res = gen_product(t, it)
        self.assertEqual(res.template, 'a aa c | a ab c | a ba c | a bb c | ')

    def test_3_value_mod_2(self):
        t = Template('a ${id} c | ')
        it = Iterable(
            key='id',
            vals=['a', 'b', 'c'],
            itermode=Itermode.product,
            iter_modifier=2)
        res = gen_product(t, it)
        self.assertEqual(
            res.template,
            'a aa c | a ab c | a ac c | a ba c | a bb c | a bc c | a ca c | a cb c | a cc c | '
        )


class TestDispatchIterations(unittest.TestCase):
    def test_comb_one_key_one_iter(self):
        t = Template('a ${id} d | ')
        its = [
            Iterable(
                key='id',
                vals=['b', 'c'],
                itermode=Itermode.combinations,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'a bc d | ')

    def test_combWR_one_key_one_iter(self):
        t = Template('a ${id} d | ')
        its = [
            Iterable(
                key='id',
                vals=['b', 'c'],
                itermode=Itermode.combinationsWR,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'a bb d | a bc d | a cc d | ')

    def test_perm_one_key_one_iter(self):
        t = Template('a ${id} d | ')
        its = [
            Iterable(
                key='id',
                vals=['b', 'c'],
                itermode=Itermode.permutations,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'a bc d | a cb d | ')

    def test_product_one_key_one_iter(self):
        t = Template('a ${id} d | ')
        its = [
            Iterable(
                key='id',
                vals=['b', 'c'],
                itermode=Itermode.product,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'a bb d | a bc d | a cb d | a cc d | ')

    def test_comb_two_key_one_iter(self):
        t = Template("${id1} ${id2} | ")
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.combinations,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'bc ${id2} | ')

    def test_combWR_two_key_one_iter(self):
        t = Template("${id1} ${id2} | ")
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.combinationsWR,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'bb ${id2} | bc ${id2} | cc ${id2} | ')

    def test_perm_two_key_one_iter(self):
        t = Template("${id1} ${id2} | ")
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.permutations,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'bc ${id2} | cb ${id2} | ')

    def test_prod_two_key_one_iter(self):
        t = Template("${id1} ${id2} | ")
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.product,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template,
                         'bb ${id2} | bc ${id2} | cb ${id2} | cc ${id2} | ')

    def test_comb_two_key_two_iter(self):
        t = Template('${id1} ${id2} | ')
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.combinations,
                iter_modifier=2),
            Iterable(
                key='id2',
                vals=['d', 'e'],
                itermode=Itermode.combinations,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'bc de | ')

    def test_combWR_two_key_two_iter(self):
        t = Template('${id1} ${id2} | ')
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.combinationsWR,
                iter_modifier=2),
            Iterable(
                key='id2',
                vals=['d', 'e'],
                itermode=Itermode.combinationsWR,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(
            res.template,
            'bb dd | bc dd | cc dd | bb de | bc de | cc de | bb ee | bc ee | cc ee | '
        )

    def test_perm_two_key_two_iter(self):
        t = Template('${id1} ${id2} | ')
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.permutations,
                iter_modifier=2),
            Iterable(
                key='id2',
                vals=['d', 'e'],
                itermode=Itermode.permutations,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(res.template, 'bc de | cb de | bc ed | cb ed | ')

    def test_prod_two_key_two_iter(self):
        t = Template('${id1} ${id2} | ')
        its = [
            Iterable(
                key='id1',
                vals=['b', 'c'],
                itermode=Itermode.product,
                iter_modifier=2),
            Iterable(
                key='id2',
                vals=['d', 'e'],
                itermode=Itermode.product,
                iter_modifier=2)
        ]
        res = dispatch_iterations(t, its)
        self.assertEqual(
            res.template,
            'bb dd | bc dd | cb dd | cc dd | bb de | bc de | cb de | cc de | bb ed | bc ed | cb ed | cc ed | bb ee | bc ee | cb ee | cc ee | '
        )

    def test_comma_iters(self):
        t = Template('${id0} | ')
        comb_iter = Iterable(
            key='id0',
            vals=['a', 'b'],
            itermode=Itermode.combinations,
            iter_modifier=2,
            comma_list=True)
        combWR_iter = Iterable(
            key='id0',
            vals=['a', 'b'],
            itermode=Itermode.combinationsWR,
            iter_modifier=2,
            comma_list=True)
        perm_iter = Iterable(
            key='id0',
            vals=['a', 'b'],
            itermode=Itermode.permutations,
            iter_modifier=2,
            comma_list=True)
        prod_iter = Iterable(
            key='id0',
            vals=['a', 'b'],
            itermode=Itermode.product,
            iter_modifier=2,
            comma_list=True)
        comb_res = dispatch_iterations(t, [comb_iter])
        combWR_res = dispatch_iterations(t, [combWR_iter])
        perm_res = dispatch_iterations(t, [perm_iter])
        prod_res = dispatch_iterations(t, [prod_iter])
        self.assertEqual(comb_res.template, 'a, b | ')
        self.assertEqual(combWR_res.template, 'a, a | a, b | b, b | ')
        self.assertEqual(perm_res.template, 'a, b | b, a | ')
        self.assertEqual(prod_res.template, 'a, a | a, b | b, a | b, b | ')


class TestCombinedDispatchIterations(unittest.TestCase):
    def test_gen_combinations_list(self):
        iterable = Iterable(
            'key_test', ['1', '2', '3'],
            itermode=Itermode.combinations,
            iter_modifier=2)
        self.assertEqual(('key_test', ['12', '13', '23']),
                         gen_combinations_list(iterable))

    def test_gen_combinations_with_replacement_list(self):
        iterable = Iterable(
            'key_test', ['1', '2', '3'],
            itermode=Itermode.combinationsWR,
            iter_modifier=2)
        self.assertEqual(('key_test', ['11', '12', '13', '22', '23', '33']),
                         gen_combinations_with_replacement_list(iterable))

    def test_gen_permutations_list(self):
        iterable = Iterable(
            'key_test', ['1', '2', '3'],
            itermode=Itermode.permutations,
            iter_modifier=2)
        self.assertEqual(('key_test', ['12', '13', '21', '23', '31', '32']),
                         gen_permutations_list(iterable))

    def test_gen_product_list(self):
        iterable = Iterable(
            'key_test', ['1', '2', '3'],
            itermode=Itermode.product,
            iter_modifier=2)
        self.assertEqual(
            ('key_test',
             ['11', '12', '13', '21', '22', '23', '31', '32', '33']),
            gen_product_list(iterable))

    def test_combined_dispatcher(self):
        iterables = [
            Iterable('key0', ['1', '2', '3'], Itermode.combinations, 2),
            Iterable('key1', ['a', 'b', 'c'], Itermode.combinations, 2, True)
        ]
        template = Template('${key0}  ${key1}  | ')
        self.assertEqual('12  a, b  | 13  a, c  | 23  b, c  | ',
                         combined_dispatcher(template, iterables).template)

        iterables2 = [
            Iterable('key0', ['1', '2', '3'], Itermode.product, 2),
            Iterable('key1', ['a', 'b', 'c'], Itermode.product, 2, True)
        ]
        template2 = Template('${key0}  ${key1}  | ')
        self.assertEqual(
            '11  a, a  | 12  a, b  | 13  a, c  | 21  b, a  | 22  b, b  | 23  b,\
 c  | 31  c, a  | 32  c, b  | 33  c, c  | ',
            combined_dispatcher(template2, iterables2).template)

    def test_removal_dispatcher(self):
        in_iterables = [
            Iterable('key0', ['1', '2', '3'], Itermode.product, 2),
            Iterable('key1', ['a', 'b', 'c'], Itermode.product, 2, True)
        ]
        removal_iterables = [
            Iterable('', ['1', '2'], Itermode.product, 2),
            Iterable('', ['a', 'b'], Itermode.product, 2, True)
        ]
        template = Template('${key0}  ${key1}  | ')
        self.assertEqual(
            '13  a, c  | 23  a, c  | 31  a, c  | 32  a, c  | 33  a, c  | 13  b,\
 c  | 23  b, c  | 31  b, c  | 32  b, c  | 33  b, c  | 13  c, a  | 23  c, a  | 3\
1  c, a  | 32  c, a  | 33  c, a  | 13  c, b  | 23  c, b  | 31  c, b  | 32  c, b\
  | 33  c, b  | 13  c, c  | 23  c, c  | 31  c, c  | 32  c, c  | 33  c, c  | ',
            removal_dispatcher(template, in_iterables,
                               removal_iterables).template)

    def test_combined_removal_dispatcher(self):
        in_iterables = [
            Iterable('key0', ['1', '2', '3'], Itermode.product, 2),
            Iterable('key1', ['a', 'b', 'c'], Itermode.product, 2, True)
        ]
        removal_iterables = [
            Iterable('', ['1', '2'], Itermode.product, 2),
            Iterable('', ['a', 'b'], Itermode.product, 2, True)
        ]
        template = Template('${key0}  ${key1}  | ')
        # This is wrong. Should only have instances of [1,3], [2,3], [a,c], [b,c]
        self.assertEqual(
            '13  a, c  | 23  b, c  | 31  c, a  | 32  c, b  | 33  c, c  | ',
            combined_removal_dispatcher(template, in_iterables,
                                        removal_iterables).template)


def run_iter_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIters)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGenCombinationsWR)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGenPermutations)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGenProduct)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDispatchIterations)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestCombinedDispatchIterations)
    unittest.TextTestRunner().run(suite)
