import unittest

from parsers.earley.earley_recognizer import *


class TestEarleyParser(unittest.TestCase):
    """
    Tests for simple Earley recognizer.
    """

    def test_simple_grammar(self):
        lexicon = read_lexicon('data/lexicon.txt')
        grammar = read_grammar('data/grammar.txt')
        parser = EarleyRecognizer(grammar, lexicon)
        tokens = ['Peter', 'likes', 'hot', 'coffee']

        part_of_lang = parser.recognize(tokens)

        self.assertTrue(part_of_lang)

    def test_left_recursion(self):
        lexicon = read_lexicon('data/simple_lexicon.txt')
        grammar = read_grammar('data/left-recursive_grammar.txt')
        parser = EarleyRecognizer(grammar, lexicon)
        tokens = ['a', 'a', 'a', 'a']

        part_of_lang = parser.recognize(tokens)

        self.assertTrue(part_of_lang)

    def test_espresso_grammar(self):
        """
        Example grammar taken from Chris Culy's 2013 parsing course.
        """
        lexicon = read_lexicon('data/lexicon-espresso.txt')
        grammar = read_grammar('data/grammar-espresso.txt')
        parser = EarleyRecognizer(grammar, lexicon)
        tokens = ['Yesterday', 'Chris', 'drank', 'an', 'espresso']

        part_of_lang = parser.recognize(tokens)

        self.assertTrue(part_of_lang)


if __name__ == '__main__':
    unittest.main()
