import json
from parsers.top_down import TopDownParser
from parsers.shared import read_grammar


def dfs_search_all_steps(graph, start):
    visited, stack = {}, [start]
    steps, i = [], 0
    while stack:
        vertex = stack.pop()
        i += 1
        step = {'id': i, 'position': vertex.ind, 'prediction': vertex.predictions, 'isGoal': False}
        if vertex.parent:
            step['parentId'] = visited[vertex.parent]
        if vertex.rule:
            step["rule"] = str(vertex.rule)
        if graph.is_goal(vertex):
            step['isGoal'] = True
        steps.append(step)
        if vertex not in visited:
            visited[vertex] = i
            stack.extend(graph.successors(vertex) - visited.keys())
    return steps


def write(text, path):
    with open(path, mode='wb') as fout:
        fout.write(text.encode("UTF-8"))


if __name__ == '__main__':

    tokens = 'a a b b a b'.split()
    grammar_path = 'data/greibach_normal_form_grammar.txt'
    grammar = read_grammar(grammar_path)
    parser = TopDownParser(grammar)

    steps = parser.parse(tokens, dfs_search_all_steps)
    json_steps = json.dumps(steps, indent=4, sort_keys=True)
    write(json_steps, 'vis/top-down/' + '-'.join(tokens) + '.json')