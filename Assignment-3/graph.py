from typing import Any

"""
Graph is a directed, weighted graph stored as an adjacency map:
each source vertex maps to a dict of {destination: cost}.
A vertex is only recorded once it has at least one outgoing edge.
"""

class Graph:
    def __init__(self) -> None:
        self.vertices: dict[Any,dict[Any,Any]] = {}

    def get_vertices(self) -> dict[Any,dict[Any,Any]]:
        """
        return the adjacency map of every vertex that has outgoing edges
        """
        return self.vertices

    def add_edge(self, source: Any, destination: Any, cost: float):
        """
        Add a directed edge from [source] to [destination] with the given cost.
        If the edge already exists, its cost is replaced.
        param source the vertex the edge starts from
        param destination the vertex the edge points to
        param cost the weight of the edge
        """
        if source not in self.vertices:
            self.vertices[source] = {}

        self.vertices[source][destination] = cost

    def get_edges(self, source: Any):
        """
        Get the outgoing edges of [source].
        return a dict of {destination: cost}, or None if [source] has no outgoing edges
        """
        if source in self.vertices:
            return self.vertices[source]

    def clear(self):
        """
        Remove every vertex and edge from the graph
        """
        self.vertices = {}
