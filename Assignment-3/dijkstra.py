from graph import Graph
from priority_queue import Min_Priority_Queue
from typing import Any

def dijkstra(graph: Graph, start: Any, target: Any):
    """
    Find the cheapest path from [start] to [target] using Dijkstra's algorithm.
    Edge costs must be non-negative. The search stops as soon as [target]
    is reached, so vertices further away than [target] are never explored.
    param graph the directed, weighted graph to search
    param start the vertex the path begins at
    param target the vertex the path ends at
    return a tuple (cost, path) where path is the list of vertices from
    [start] to [target] inclusive, or (inf, None) if [target] cannot be reached
    """
    to_do = Min_Priority_Queue()
    costs: dict[Any, Any] = {start: 0}
    previous: dict[Any, Any] = {start: None}  # the vertex each one was reached from
    to_do.add_with_priority(start,0)

    while not to_do.is_empty():
        u, weight = to_do.next_elem()

        if u == target:
            path: list[Any] = []
            while u is not None:
                path.append(u)
                u = previous[u]
            path.reverse()
            return weight, path

        for n, w in (graph.get_edges(u) or {}).items():
            new_cost = weight + w

            if new_cost < costs.get(n, float('inf')):
                costs[n] = new_cost
                previous[n] = u
                to_do.adjust_priority(n,new_cost)

    return float('inf'), None
