INDENT = ' ' * 4


class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return '{} -> {}'.format(self.lhs, ' '.join(self.rhs))

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.lhs == other.lhs
                and self.rhs == other.rhs)

    @staticmethod
    def from_str(rule_str):
        fields = rule_str.split('->')
        return Rule(fields[0].strip(), tuple(fields[1].strip().split()))


def read_lexicon(path):
    lexicon = {}
    with open(path, 'r') as fin:
        for line in fin:
            rule = Rule.from_str(line)
            if rule.lhs not in lexicon:
                lexicon[rule.lhs] = []
            lexicon[rule.lhs].append(rule.rhs[0])
    return lexicon


def read_grammar(path):
    grammar = {}
    with open(path, 'r') as fin:
        for line in fin:
            rule = Rule.from_str(line)
            if rule.lhs not in grammar:
                grammar[rule.lhs] = []
            grammar[rule.lhs].append(rule)
    return grammar


def concat_tuples(t1, t2):
    l = list(t1)
    l.extend(t2)
    return tuple(l)
