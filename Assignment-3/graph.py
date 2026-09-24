from typing import Any

class Graph:
    def __init__(self) -> None:
        self.vertices: dict[Any,dict[Any,Any]] = {}

    def get_vertices(self) -> dict[Any,dict[Any,Any]]:
        return self.vertices

    def add_edge(self, source: Any, destination: Any, cost: float):
        if source not in self.vertices:
            self.vertices[source] = {}

        self.vertices[source][destination] = cost

    def get_edges(self, source: Any):
        if source in self.vertices:
            return self.vertices[source]

    def clear(self):
        self.vertices = {}