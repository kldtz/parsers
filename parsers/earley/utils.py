import collections
from functools import total_ordering


class Node:
    def __init__(self, label, start, end):
        self.label = label
        self.start = start
        self.end = end

    def __eq__(self, other):
        return (self.label == other.label and
                self.start == other.start and
                self.end == other.end)

    def __repr__(self):
        return '"{} [{},{}]"'.format(self.label, self.start, self.end)

    def span(self):
        return self.end - self.start


@total_ordering
class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return '{} -> {}'.format(self.from_node, self.to_node)

    def __eq__(self, other):
        return (self.to_node.start == other.to_node.start
                and self.to_node.span() == other.to_node.span())

    def __lt__(self, other):
        return ((self.to_node.start, other.to_node.span()) <
                (other.to_node.start, self.to_node.span()))


Deriv = collections.namedtuple("Deriv", ["edges", "families", "stack"])


def collect_derivations(sppf):
    unfinished = [Deriv([], set(), [sppf])]
    finished = []
    while unfinished:
        deriv = unfinished.pop()
        while deriv.stack:
            sppf = deriv.stack.pop()
            if not sppf:
                continue
            if len(sppf.families) > 1:
                for family in sppf.families[1:]:
                    if family in deriv.families:
                        continue
                    new_deriv = Deriv(list(deriv.edges), set(
                        deriv.families), list(deriv.stack))
                    _add_family(new_deriv, sppf, family)
                    unfinished.append(new_deriv)
            if len(sppf.families) > 0:
                first_family = sppf.families[0]
                if first_family not in deriv.families:
                    _add_family(deriv, sppf, first_family)
        finished.append(deriv.edges)
    return finished


def _add_family(deriv, sppf, family):
    deriv.families.add(family)
    root = Node(sppf.item, sppf.start, sppf.end)
    if family.left:
        left_edge = Edge(root, Node(family.left.item,
                                    family.left.start, family.left.end))
        deriv.edges.append(left_edge)
    deriv.stack.append(family.left)
    right_edge = Edge(root, Node(family.right.item,
                                 family.right.start, family.right.end))
    deriv.edges.append(right_edge)
    deriv.stack.append(family.right)


def to_dot_language(tree, name):
    tree.sort()
    lines = ['digraph ' + name + ' {']
    for edge in tree:
        lines.append('\t' + str(edge) + ';')
    lines.append('}')
    return '\n'.join(lines)
