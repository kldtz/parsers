import logging
from functools import wraps

from parsers.shared import Rule, read_lexicon, read_grammar, INDENT


class State:
    def __init__(self, rule, dot, span):
        self.rule = rule
        self.dot = dot
        self.span = span

    def __repr__(self):
        rhs = list(self.rule.rhs)
        rhs.insert(self.dot, '.')
        return '{} -> {} [{}, {}]'.format(self.rule.lhs, ' '.join(rhs), self.start, self.end)

    def __hash__(self):
        return hash((self.rule, self.dot, self.span))

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.rule == other.rule
                and self.dot == other.dot
                and self.span == other.span)

    @property
    def start(self):
        return self.span[0]

    @property
    def end(self):
        return self.span[1]

    @property
    def lhs(self):
        return self.rule.lhs

    @property
    def is_complete(self):
        return self.dot == len(self.rule.rhs)

    @property
    def next_cat(self):
        return self.rule.rhs[self.dot]


def log(func):
    @wraps(func)
    def wrapper(s, state):
        f_string = '{}({})'
        if func.__name__ == 'enqueue':
            f_string = INDENT + f_string
        logging.info(f_string.format(func.__name__, state))
        func(s, state)

    return wrapper


class EarleyRecognizer:
    """
    Earley recognizer implementation for educational purposes following
    pseudo code from Jurafsky and Martin (2009, p. 478).
    """

    def __init__(self, grammar, lexicon):
        self.grammar = grammar
        self.lexicon = lexicon
        self.states = None
        self.chart = None
        self.tokens = None

    def recognize(self, tokens):
        self.states = set()
        self.chart = [[] for _ in range(len(tokens) + 1)]
        self.tokens = tokens
        self.enqueue(State(Rule.from_str('START -> S'), 0, (0, 0)))
        for i in range(len(self.chart)):
            for state in self.chart[i]:
                if not state.is_complete:
                    if state.next_cat not in self.lexicon:
                        self.predict(state)
                    else:
                        self.scan(state)
                else:
                    self.complete(state)
        return self.has_parse()

    @log
    def enqueue(self, state):
        if state not in self.states:
            self.chart[state.end].append(state)
            self.states.add(state)

    @log
    def predict(self, state):
        for rule in self.grammar[state.next_cat]:
            self.enqueue(State(Rule(state.next_cat, rule.rhs),
                               0, (state.end, state.end)))

    @log
    def scan(self, state):
        if (state.end < len(self.tokens) and state.next_cat in self.lexicon
                and self.tokens[state.end] in self.lexicon[state.next_cat]):
            self.enqueue(State(state.rule, state.dot + 1,
                               (state.start, state.end + 1)))

    @log
    def complete(self, state):
        for entry in self.chart[state.start]:
            if not entry.is_complete and entry.next_cat == state.lhs:
                self.enqueue(State(entry.rule, entry.dot +
                                   1, (entry.start, state.end)))

    def has_parse(self):
        for state in self.chart[-1]:
            if state.lhs == 'S' and state.is_complete:
                return True
        return False


def recognize(tokens, grammar_path, lexicon_path):
    logging.info('\nTokens: ' + str(tokens))
    logging.info('Loading lexicon and grammar...')
    lexicon = read_lexicon(lexicon_path)
    grammar = read_grammar(grammar_path)
    parser = EarleyRecognizer(grammar, lexicon)

    logging.info('\nRunning Earley algorithm...')
    part_of_lang = parser.recognize(tokens)
    logging.info('\nSentence is part of the language: ' + str(part_of_lang))
    logging.info('\nEarley sets:')
    for i, state_set in enumerate(parser.chart):
        logging.info('State set {}:'.format(str(i)))
        logging.info('\n'.join([INDENT + str(state) for state in state_set]))
