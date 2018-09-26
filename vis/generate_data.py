import json

from parsers.shared import read_grammar
from parsers.top_down import TopDownParser


def dfs_search_all_tree(graph, start):
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
            new_vertices = graph.successors(vertex) - visited.keys()
            stack.extend(sorted(new_vertices, key=lambda x: ''.join(x.predictions), reverse=True))
    return steps


def dfs_search_all_dag(graph, start):
    visited, stack = {}, [(start, None)]
    i = 0
    while stack:
        vertex, parent_id = stack.pop()
        if vertex not in visited:
            i += 1
            json_node = {"id": i, "position": vertex.ind, "isGoal": False, "parents": [parent_id],
                         'prediction': vertex.predictions}
            if graph.is_goal(vertex):
                json_node["isGoal"] = True
            if vertex.rule:
                json_node["rule"] = str(vertex.rule)
            stack.extend([(successor, i) for successor in
                          sorted(graph.successors(vertex), key=lambda x: ''.join(x.predictions), reverse=False)])
            visited[vertex] = json_node
        else:
            visited[vertex]["parents"].append(parent_id)
    return visited.values()


def write(text, path):
    with open(path, mode='wb') as fout:
        fout.write(text.encode("UTF-8"))


if __name__ == '__main__':
    tokens = 'a a b b a b'.split()
    grammar_path = 'data/greibach_normal_form_grammar.txt'
    grammar = read_grammar(grammar_path)
    parser = TopDownParser(grammar)

    vertices = sorted(parser.parse(tokens, dfs_search_all_dag), key=lambda x: x["id"])
    json_steps = json.dumps(vertices, indent=4, sort_keys=True)
    write(json_steps, 'vis/top-down/dag-data/' + '-'.join(tokens) + '-lexicographic-reverse.json')
