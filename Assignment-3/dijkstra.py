from graph import Graph
from priority_queue import Min_Priority_Queue
from typing import Any

def dijkstra(graph: Graph, start: Any):
    """
    Find the cheapest path cost from [start] to every vertex reachable from it,
    using Dijkstra's algorithm. Edge costs must be non-negative.
    param graph the directed, weighted graph to search
    param start the vertex to measure all costs from
    return a dict mapping each vertex to its cheapest cost from [start].
    Vertices with outgoing edges that cannot be reached map to infinity;
    vertices with no outgoing edges appear only if they are reached.
    """
    to_do = Min_Priority_Queue()
    costs: dict[Any, Any] = {node: float('inf') for node in graph.get_vertices()}
    costs[start] = 0
    to_do.add_with_priority(start,0)

    while not to_do.is_empty():
        u, weight = to_do.next_elem()
        if weight > costs[u]:
            continue

        for n, w in (graph.get_edges(u) or {}).items():
            new_cost = weight + w

            if new_cost < costs.get(n, float('inf')):
                costs[n] = new_cost
                to_do.adjust_priority(n,new_cost)

    return costs