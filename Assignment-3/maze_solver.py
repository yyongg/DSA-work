from dijkstra import dijkstra
from graph import Graph

def find_cell(maze: list[str], char: str):
    """
    return the (row, column) of the first occurrence of [char] in the maze,
    or None if it does not appear
    """
    for i, row in enumerate(maze):
        j = row.find(char)
        if j != -1:
            return i, j
    return None

def build_graph(maze: list[str]):
    """
    Turn the maze into a graph: each open cell (row, column) is a vertex,
    with an edge of cost 1 to each open cell above, below, left and right of it.
    param maze the rows of the maze
    return the graph
    """
    graph = Graph()
    n = len(maze)

    for i in range(n):
        for j in range(len(maze[i])):
            if maze[i][j] == '#':
                continue

            # only look right and down; adding both directions covers left and up
            for ni, nj in ((i + 1, j), (i, j + 1)):
                if ni < n and nj < len(maze[ni]) and maze[ni][nj] != '#':
                    graph.add_edge((i, j), (ni, nj), 1)
                    graph.add_edge((ni, nj), (i, j), 1)

    return graph

def solve_maze(maze: list[str]):
    """
    Find a shortest path from 'S' to 'T' by running dijkstra on the maze's graph.
    param maze the rows of the maze
    return the list of (row, column) cells from 'S' to 'T' inclusive,
    or None if there is no path
    """
    start = find_cell(maze, 'S')
    end = find_cell(maze, 'T')
    if start is None or end is None:
        return None

    _, path = dijkstra(build_graph(maze), start, end)
    return path
