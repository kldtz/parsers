import logging
from functools import wraps

from .graph_search import Graph
from .shared import concat_tuples, read_grammar, INDENT


class TopDownConfig:
    def __init__(self, ind, predictions, rule, parent):
        self.ind = ind
        self.predictions = predictions
        self.rule = rule
        self.parent = parent

    def __repr__(self):
        return '{}: {}'.format(self.ind, self.predictions)

    @property
    def prediction(self):
        if self.predictions:
            return self.predictions[0]
        return None

    @property
    def derivation(self):
        rules = []
        config = self
        while config:
            if config.rule:
                rules.insert(0, config.rule)
            config = config.parent
        return rules


def log(func):
    @wraps(func)
    def wrapper(s, state):
        f_string = '{}({})'
        if func.__name__ == '_match':
            f_string = INDENT + f_string
        logging.info(f_string.format(func.__name__.strip('_'), state))
        rval = func(s, state)
        f_string = INDENT + 'rval: {}'
        if func.__name__ == '_match':
            f_string = INDENT + f_string
        logging.info(f_string.format(rval))
        return rval

    return wrapper


class TopDownParser(Graph):
    """
    Naive top-down parser implementation.
    """

    def __init__(self, grammar):
        self.grammar = grammar
        self.input = None

    def parse(self, input, search):
        self.input = input
        start_config = TopDownConfig(0, ('S',), None, None)
        return search(self, start_config)

    def successors(self, config):
        if config.prediction in self.grammar:
            return self._predict(config)
        return self._match(config)

    def is_goal(self, config):
        return not config.prediction and len(self.input) == config.ind

    @log
    def _match(self, config):
        if config.ind < len(self.input) and config.prediction == self.input[config.ind]:
            return {TopDownConfig(config.ind + 1, config.predictions[1:], None, config)}
        return set()

    @log
    def _predict(self, config):
        configs = []
        for rule in self.grammar[config.prediction]:
            configs.append(TopDownConfig(config.ind, concat_tuples(rule.rhs, config.predictions[1:]), rule, config))
        return set(configs)


def parse(tokens, grammar_path, search):
    logging.info('\nTokens: ' + str(tokens))
    logging.info('Loading lexicon and grammar...')
    grammar = read_grammar(grammar_path)
    logging.info('\nRunning top-down parser...')
    parser = TopDownParser(grammar)

    configs = parser.parse(tokens, search)
    if not configs:
        logging.info('\nString is not part of the language!')
        return
    if not type(configs) is list:
        configs = [configs]
    for i, config in enumerate(configs):
        logging.info('\nDerivation {}:'.format(i + 1))
        logging.info(config.derivation)
