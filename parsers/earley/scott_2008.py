import collections

Rule = collections.namedtuple("Rule", ["lhs", "rhs"])
Family = collections.namedtuple("Family", ["left", "right"])
EPSILON = 'eps'


class Item:
    def __init__(self, rule, dot):
        self.rule = rule
        self.dot = dot

    def __repr__(self):
        rhs = list(self.rule.rhs)
        rhs.insert(self.dot, '.')
        rhs_string = ' '.join(rhs)
        return '{} -> {}'.format(self.rule.lhs, rhs_string)

    def __hash__(self):
        return hash((self.rule, self.dot))

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.rule == other.rule
                and self.dot == other.dot)


class ParserItem:
    def __init__(self, item, start, sppf):
        self.item = item
        self.start = start
        self.sppf = sppf

    def __hash__(self):
        return hash((self.item, self.start, self.sppf))

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.item == other.item
                and self.start == other.start
                and self.sppf == other.sppf)

    def __repr__(self):
        return '({} [{}])'.format(self.item, self.start)

    @property
    def next(self):
        if self.is_complete():
            return None
        return self.item.rule.rhs[self.item.dot]

    def is_complete(self):
        return self.item.dot == len(self.item.rule.rhs)

    @property
    def rule(self):
        return self.item.rule

    @property
    def lhs(self):
        return self.item.rule.lhs

    @property
    def dot(self):
        return self.item.dot


class SPPF:
    def __init__(self, item, start, end):
        self.item = item
        self.start = start
        self.end = end
        self.families = []

    def add_family(self, family):
        if family not in self.families:
            self.families.append(family)

    def __hash__(self):
        return hash((self.item, self.start, self.end))

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.item == other.item
                and self.start == other.start
                and self.end == other.end)

    def __repr__(self):
        return '({}-{}: {})'.format(self.start, self.end, self.item)


def get_rules(grammar, nt):
    if not nt in grammar:
        return []
    return grammar[nt]


class Chart:
    def __init__(self, tokens):
        self.tokens = tokens
        self.chart = [set() for _ in range(len(tokens) + 1)]
        self.next_scannables = set()
        self.curr_nodes = {}

    def get_token(self, i):
        if i >= len(self.tokens):
            return "<END>"
        else:
            return self.tokens[i]

    def advance(self, i):
        self.empty_derivations = {}
        self.new_items = set(self.chart[i])
        self.scannables = set(self.next_scannables)
        self.next_scannables = set()

    def _is_scannable(self, item, i):
        return i < len(self.tokens) and item.next == self.tokens[i]

    def completable_items(self, lhs, i):
        completable = []
        for item in self.chart[i]:
            if item.next == lhs:
                completable.append(item)
        return completable

    def add_next_item(self, item, i):
        if self._is_scannable(item, i):
            self.next_scannables.add(item)
        elif i < len(self.chart) and item not in self.chart[i]:
            self.chart[i].add(item)

    def add_curr_item(self, item, i):
        if self._is_scannable(item, i):
            self.scannables.add(item)
        elif i < len(self.chart) and item not in self.chart[i]:
            self.chart[i].add(item)
            self.new_items.add(item)

    def find_root(self):
        for item in self.chart[-1]:
            if item.lhs == 'S' and item.is_complete() and item.start == 0:
                return item.sppf
        return None


def parse(grammar, tokens):
    if len(tokens) == 0:
        return None
    chart = Chart(tokens)
    start_item = ParserItem(Item(Rule('START', ('S',)), 0), 0, None)
    chart.add_next_item(start_item, 0)

    for i in range(len(tokens) + 1):
        chart.advance(i)
        while chart.new_items:
            curr = chart.new_items.pop()
            if not curr.is_complete():
                predict(grammar, chart, curr.next, i)
                if curr.next in chart.empty_derivations:  # next is empty derivation
                    adv_item = advance(
                        chart, curr, i, chart.empty_derivations[curr.next])
                    chart.add_curr_item(adv_item, i)
            else:
                if curr.sppf == None:
                    curr.sppf = make_empty_node(chart, curr.lhs, i)
                if curr.start == i:
                    chart.empty_derivations[curr.lhs] = curr.sppf
                complete(chart, curr, i)
        chart.curr_nodes = {}
        scan(chart, i)
    return chart.find_root()


def predict(grammar, chart, lhs, i):
    for rule in get_rules(grammar, lhs):
        chart.add_curr_item(ParserItem(Item(rule, 0), i, None), i)


def scan(chart, i):
    token_sppf = SPPF(chart.get_token(i), i, i + 1)
    while chart.scannables:
        item = chart.scannables.pop()
        adv_item = advance(chart, item, i + 1, token_sppf)
        chart.add_next_item(adv_item, i + 1)


def complete(chart, curr, i):
    for item in chart.completable_items(curr.lhs, curr.start):
        adv_item = advance(chart, item, i, curr.sppf)
        chart.add_curr_item(adv_item, i)


def advance(chart, completable, i, right_sppf):
    adv_item = Item(completable.rule, completable.dot + 1)  # move dot
    y = make_node(chart, adv_item, completable.start, i,
                  completable.sppf, right_sppf)  # create SPPF node
    return ParserItem(adv_item, completable.start, y)  # create new item


def make_empty_node(chart, lhs, i):
    empty_node = SPPF(lhs, i, i)
    if empty_node in chart.curr_nodes:
        empty_node = chart.curr_nodes[empty_node]
    else:
        chart.curr_nodes[empty_node] = empty_node
    epsilon_sppf = SPPF(EPSILON, i, i)
    empty_node.add_family(Family(None, epsilon_sppf))
    return empty_node


def make_node(chart, item, start, end, left, right):
    s = item.rule.lhs
    if item.dot != len(item.rule.rhs):  # item is not complete
        if item.dot == 1:
            return right
        s = item
    sppf = SPPF(s, start, end)
    if sppf not in chart.curr_nodes:
        chart.curr_nodes[sppf] = sppf
    sppf = chart.curr_nodes[sppf]
    if (left == None):
        sppf.add_family(Family(None, right))
    else:
        sppf.add_family(Family(left, right))
    return sppf
