from typing import Any
from path_check import dfs, bfs

graph: dict[Any, Any] = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': ['E'],
    'E': [],
}

print(dfs(graph, 'A', 'E'))   # True
print(dfs(graph, 'E', 'A'))   # False  (edges are one-directional)

print(bfs(graph, 'A', 'E'))   # True
print(dfs(graph, 'E', 'A'))   # False  (edges are one-directional)
