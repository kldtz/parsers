import os
import re
import unittest

from parsers.earley.scott_2008 import *
from parsers.earley.utils import collect_derivations, to_dot_language


class TestEarleyParser(unittest.TestCase):
    '''
    Tests for Earley parser implementation following Scott (2008). 

    Use 'python -m unittest tests.test_scott_2008' from the project's root 
    directory to run the tests.
    '''
    TEST_RESOURCES = 'data'

    def assert_string_equals(self, filename, actual_string, message=None):
        with open(os.path.join(self.TEST_RESOURCES, filename), 'r') as f:
            expected_string = re.sub(r'^\s+', '', f.read(), flags=re.M)
            self.assertEqual(expected_string, re.sub(
                r'^\s+', '', actual_string, flags=re.M), message)

    def test_first_example(self):
        grammar = {'S': [Rule('S', ('S', 'T')), Rule('S', ('a',))], 'B': [
            Rule('B', ())], 'T': [Rule('T', ('a', 'B')), Rule('T', ('a',))]}
        tokens = ['a', 'a']

        forest = parse(grammar, tokens)
        trees = collect_derivations(forest)
        trees.sort(key=len)  # set order is not deterministic

        self.assertEqual(2, len(trees))
        self.assertEqual(4, len(trees[0]))
        actual_string = to_dot_language(trees[0], 'tree1')
        self.assert_string_equals(
            'first_example/tree1.gv', actual_string)

        self.assertEqual(6, len(trees[1]))
        actual_string = to_dot_language(trees[1], 'tree2')
        self.assert_string_equals(
            'first_example/tree2.gv', actual_string)

    def test_simple_recursion(self):
        grammar = {'S': [Rule('S', ('S', 'S')), Rule('S', ('b',))]}
        tokens = ['b', 'b', 'b']

        forest = parse(grammar, tokens)
        trees = collect_derivations(forest)

        self.assertEqual(2, len(trees), 'Number of trees')
        self.assertEqual(7, len(trees[0]))
        self.assertEqual(7, len(trees[1]))
        actual_string = to_dot_language(trees[0], 'tree1')
        self.assert_string_equals('simple_recursion/tree1.gv', actual_string)
        actual_string = to_dot_language(trees[1], 'tree2')
        self.assert_string_equals('simple_recursion/tree2.gv', actual_string)

    def test_hidden_left_recursion_and_cycle(self):
        grammar = {'S': [Rule('S', ('A', 'T')), Rule('S', ('a', 'T'))], 'A': [Rule('A', ('a',)), Rule(
            'A', ('B', 'A'))], 'B': [Rule('B', ())], 'T': [Rule('T', ('b', 'b', 'b'))]}
        tokens = ['a', 'b', 'b', 'b']

        forest = parse(grammar, tokens)
        trees = collect_derivations(forest)
        trees.sort(key=len)  # set order is not deterministic

        self.assertEqual(3, len(trees))
        self.assertEqual(6, len(trees[0]))
        actual_string = to_dot_language(trees[0], 'tree1')
        self.assert_string_equals(
            'hidden_left_recursion_and_cycle/tree1.gv', actual_string)

        self.assertEqual(7, len(trees[1]))
        actual_string = to_dot_language(trees[1], 'tree2')
        self.assert_string_equals(
            'hidden_left_recursion_and_cycle/tree2.gv', actual_string)

        self.assertEqual(10, len(trees[2]))
        actual_string = to_dot_language(trees[2], 'tree3')
        self.assert_string_equals(
            'hidden_left_recursion_and_cycle/tree3.gv', actual_string)


if __name__ == '__main__':
    unittest.main()
