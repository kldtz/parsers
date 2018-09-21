from abc import ABC, abstractmethod


class Graph(ABC):
    @abstractmethod
    def successors(self, vertex):
        pass

    @abstractmethod
    def is_goal(self, vertex):
        pass


def bfs_search_first(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if graph.is_goal(vertex):
            return vertex
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph.successors(vertex) - visited)
    return None


def bfs_search_all(graph, start):
    vertices = []
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if graph.is_goal(vertex):
            return vertices.append(vertex)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph.successors(vertex) - visited)
    return vertices


def dfs_search_first(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if graph.is_goal(vertex):
            return vertex
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph.successors(vertex) - visited)
    return None


def dfs_search_all(graph, start):
    vertices = []
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if graph.is_goal(vertex):
            return vertices.append(vertex)
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph.successors(vertex) - visited)
    return vertices
