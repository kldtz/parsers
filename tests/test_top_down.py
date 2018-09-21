import unittest

from parsers.top_down import TopDownParser
from parsers.shared import read_grammar, Rule
from parsers.graph_search import bfs_search_first, dfs_search_first


class TestTopDown(unittest.TestCase):
    """
    Tests for top-down parser.
    """

    def test_bfs(self):
        grammar = read_grammar('tests/data/greibach_normal_form_grammar.txt')
        parser = TopDownParser(grammar)
        tokens = ['a', 'a', 'b', 'b']

        config = parser.parse(tokens, bfs_search_first)

        expected = ['S -> a B', 'B -> a B B', 'B -> b', 'B -> b']
        expectedRules = [Rule.from_str(s) for s in expected]
        self.assertListEqual(expectedRules, config.derivation)

    def test_dfs(self):
        grammar = read_grammar('tests/data/greibach_normal_form_grammar.txt')
        parser = TopDownParser(grammar)
        tokens = ['a', 'a', 'b', 'b']

        config = parser.parse(tokens, dfs_search_first)

        expected = ['S -> a B', 'B -> a B B', 'B -> b', 'B -> b']
        expectedRules = [Rule.from_str(s) for s in expected]
        self.assertListEqual(expectedRules, config.derivation)


if __name__ == '__main__':
    unittest.main()
