import re


class Graph:
    def __init__(self):
        self.edges = []

    def add_edge(self, u, v):
        self.edges.append((u, v))

    def has_edge(self, u, v):
        return (u, v) in self.edges


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.stack:
            return self.stack.pop(0)
        return None

    def peek(self):
        if self.stack:
            return self.stack[0]
        return None


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def string_concat(n):
    s = ""
    for i in range(n):
        s += str(i)
    return s


def matrix_sum(matrix: list[list[int]]) -> list[int]:
    return [sum(matrix[i]) for i in range(len(matrix)) if sum(matrix[i]) > 0]


def graph_traversal(graph: dict[int, dict[int]], node: int) -> dict[int]:
    visited = []

    def dfs(n: int) -> None:
        if n in visited:
            return
        visited.append(n)
        for neighbor in graph.get(n, []):
            dfs(neighbor)

    dfs(node)
    return visited


def regex_match(strings: list[str], pattern: str) -> list[str]:
    matched = []
    for s in strings:
        if re.match(pattern, s):
            matched.append(s)
    return matched


def is_palindrome(text: str) -> bool:
    cleaned_text = "".join(c.lower() for c in text if c.isalnum())
    for i in range(len(cleaned_text) // 2):
        if cleaned_text[i] != cleaned_text[len(cleaned_text) - 1 - i]:
            return False
    return True


def word_frequency(text: str) -> dict[str, int]:
    words = text.lower().split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


class PathFinder:
    def __init__(self, graph: dict[str, list[str]]):
        self.graph = graph

    def find_shortest_path(self, start: str, end: str) -> list[str]:
        if start not in self.graph or end not in self.graph:
            return []

        queue = [[start]]
        visited = set([start])

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == end:
                return path

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return []  # No path found
