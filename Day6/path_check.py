from collections import deque
from typing import Any


def bfs(graph: dict[Any, list[Any]], root: Any, target: Any):
    to_visit: set[Any] = set()
    priority_list: deque[Any] = deque()

    priority_list.appendleft(root)
    to_visit.add(root)

    while priority_list:
        n = priority_list.popleft()
        if n == target:
            return True

        for m in graph.get(n, []):
            if m not in to_visit:
                priority_list.append(m)
                to_visit.add(m)

    return False


def dfs(graph: dict[Any, list[Any]], root: Any, target: Any):
    to_visit: set[Any] = set()
    priority_list: deque[Any] = deque()

    priority_list.appendleft(root)
    to_visit.add(root)

    while priority_list:
        n = priority_list.popleft()
        if n == target:
            return True

        for m in graph.get(n, []):
            if m not in to_visit:
                priority_list.appendleft(m)
                to_visit.add(m)

    return False