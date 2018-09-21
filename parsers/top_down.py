from .graph_search import Graph
from .shared import concat_tuples


class TopDownConfig:
    def __init__(self, ind, predictions, rule, parent):
        self.ind = ind
        self.predictions = predictions
        self.rule = rule
        self.parent = parent

    def __repr__(self):
        return '{}: {}, {}'.format(self.ind, self.predictions, self.rule)

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

    def _match(self, config):
        if config.ind < len(self.input) and config.prediction == self.input[config.ind]:
            return {TopDownConfig(config.ind + 1, config.predictions[1:], None, config)}
        return set()

    def _predict(self, config):
        configs = []
        for rule in self.grammar[config.prediction]:
            configs.append(TopDownConfig(config.ind, concat_tuples(rule.rhs, config.predictions[1:]), rule, config))
        return set(configs)
