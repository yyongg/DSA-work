import random
import unittest

from dijkstra import dijkstra
from graph import Graph
from maze_solver import solve_maze


class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Graph()

    # Empty graph

    def testNewGraphHasNoVertices(self):
        self.assertEqual(self.graph.get_vertices(), {})

    def testGetEdgesUnknownSourceReturnsNone(self):
        self.assertIsNone(self.graph.get_edges("A"))

    def testClearEmptyGraphStaysEmpty(self):
        self.graph.clear()
        self.assertEqual(self.graph.get_vertices(), {})

    # One edge

    def testAddEdgeCreatesSource(self):
        self.graph.add_edge("A", "B", 1.0)
        self.assertEqual(self.graph.get_vertices(), {"A": {"B": 1.0}})

    def testGetEdgesReturnsNeighbours(self):
        self.graph.add_edge("A", "B", 1.0)
        self.assertEqual(self.graph.get_edges("A"), {"B": 1.0})

    def testSelfLoop(self):
        self.graph.add_edge("A", "A", 0.5)
        self.assertEqual(self.graph.get_edges("A"), {"A": 0.5})

    # Many edges from one source

    def testAddSecondEdgeFromSameSource(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("A", "C", 2.0)
        self.assertEqual(self.graph.get_edges("A"), {"B": 1.0, "C": 2.0})

    def testAddManyEdgesFromSameSource(self):
        for destination, cost in [("B", 1.0), ("C", 2.0), ("D", 3.0)]:
            self.graph.add_edge("A", destination, cost)
        self.assertEqual(self.graph.get_edges("A"), {"B": 1.0, "C": 2.0, "D": 3.0})

    def testReAddingEdgeUpdatesCost(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("A", "B", 2.5)
        self.assertEqual(self.graph.get_edges("A"), {"B": 2.5})

    # Many sources

    def testSeparateSourcesAreIndependent(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("C", "D", 2.0)
        self.assertEqual(self.graph.get_edges("A"), {"B": 1.0})
        self.assertEqual(self.graph.get_edges("C"), {"D": 2.0})

    def testEdgesAreDirected(self):
        # A -> B and B -> A are two different edges, with their own costs
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("B", "A", 9.0)
        self.assertEqual(self.graph.get_edges("A"), {"B": 1.0})
        self.assertEqual(self.graph.get_edges("B"), {"A": 9.0})

    def testDestinationIsNotASourceUntilItHasEdges(self):
        # Documents current behaviour: add_edge only registers the source
        self.graph.add_edge("A", "B", 1.0)
        self.assertNotIn("B", self.graph.get_vertices())
        self.assertIsNone(self.graph.get_edges("B"))

    def testChainOfEdges(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("B", "C", 2.0)
        self.graph.add_edge("C", "D", 3.0)
        self.assertEqual(
            self.graph.get_vertices(),
            {"A": {"B": 1.0}, "B": {"C": 2.0}, "C": {"D": 3.0}},
        )

    def testBranchingAndMerging(self):
        # A -> B -> D and A -> C -> D
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("A", "C", 2.0)
        self.graph.add_edge("B", "D", 3.0)
        self.graph.add_edge("C", "D", 4.0)
        self.assertEqual(self.graph.get_edges("A"), {"B": 1.0, "C": 2.0})
        self.assertEqual(self.graph.get_edges("B"), {"D": 3.0})
        self.assertEqual(self.graph.get_edges("C"), {"D": 4.0})

    # Costs

    def testZeroCost(self):
        # 0 is a real cost, not "no edge"
        self.graph.add_edge("A", "B", 0)
        self.assertEqual(self.graph.get_edges("A"), {"B": 0})

    def testNegativeCost(self):
        self.graph.add_edge("A", "B", -1.5)
        self.assertEqual(self.graph.get_edges("A"), {"B": -1.5})

    # Vertex types

    def testNonStringVertices(self):
        self.graph.add_edge(1, 2, 1.0)
        self.graph.add_edge((0, 0), (1, 1), 2.0)
        self.assertEqual(self.graph.get_edges(1), {2: 1.0})
        self.assertEqual(self.graph.get_edges((0, 0)), {(1, 1): 2.0})

    # Clearing

    def testClearRemovesEverything(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("C", "D", 2.0)
        self.graph.clear()
        self.assertEqual(self.graph.get_vertices(), {})
        self.assertIsNone(self.graph.get_edges("A"))

    def testReuseAfterClear(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.clear()
        self.graph.add_edge("X", "Y", 2.0)
        self.assertEqual(self.graph.get_vertices(), {"X": {"Y": 2.0}})

    # Scale

    def testManyEdges(self):
        for i in range(1000):
            self.graph.add_edge("A", i, float(i))
        self.assertEqual(self.graph.get_edges("A"), {i: float(i) for i in range(1000)})

    def testManySources(self):
        for i in range(1000):
            self.graph.add_edge(i, i + 1, 1.0)
        self.assertEqual(len(self.graph.get_vertices()), 1000)
        self.assertEqual(self.graph.get_edges(999), {1000: 1.0})


INF = float("inf")


class TestDijkstra(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Graph()

    def add_edges(self, edges):
        for source, destination, cost in edges:
            self.graph.add_edge(source, destination, cost)

    def path_cost(self, path):
        return sum(self.graph.get_edges(u)[v] for u, v in zip(path, path[1:]))

    # Trivial graphs

    def testStartIsTarget(self):
        self.assertEqual(dijkstra(self.graph, "A", "A"), (0, ["A"]))

    def testSingleEdge(self):
        self.add_edges([("A", "B", 3)])
        self.assertEqual(dijkstra(self.graph, "A", "B"), (3, ["A", "B"]))

    def testChain(self):
        self.add_edges([("A", "B", 1), ("B", "C", 2), ("C", "D", 3)])
        self.assertEqual(dijkstra(self.graph, "A", "D"), (6, ["A", "B", "C", "D"]))

    def testTargetPartWayAlongChain(self):
        self.add_edges([("A", "B", 1), ("B", "C", 2), ("C", "D", 3)])
        self.assertEqual(dijkstra(self.graph, "A", "C"), (3, ["A", "B", "C"]))

    # Choosing the shortest path

    def testIndirectPathBeatsDirectEdge(self):
        # A -> C costs 5 directly, but A -> B -> C costs 3
        self.add_edges([("A", "B", 1), ("B", "C", 2), ("A", "C", 5)])
        self.assertEqual(dijkstra(self.graph, "A", "C"), (3, ["A", "B", "C"]))

    def testDirectEdgeBeatsIndirectPath(self):
        self.add_edges([("A", "B", 1), ("B", "C", 2), ("A", "C", 2)])
        self.assertEqual(dijkstra(self.graph, "A", "C"), (2, ["A", "C"]))

    def testManyHopsBeatFewHops(self):
        self.add_edges([
            ("A", "Z", 100),
            ("A", "B", 1), ("B", "C", 1), ("C", "D", 1), ("D", "Z", 1),
        ])
        self.assertEqual(dijkstra(self.graph, "A", "Z"), (4, ["A", "B", "C", "D", "Z"]))

    def testCostImprovedAfterFirstDiscovery(self):
        # D is first reached via C (cost 10), then improved via B (cost 3),
        # so the path must go through B, not C
        self.add_edges([
            ("A", "C", 1), ("C", "D", 9),
            ("A", "B", 2), ("B", "D", 1),
            ("D", "E", 1),
        ])
        self.assertEqual(dijkstra(self.graph, "A", "E"), (4, ["A", "B", "D", "E"]))

    def testTiedPathsGiveSameCost(self):
        self.add_edges([("A", "B", 1), ("A", "C", 1), ("B", "D", 1), ("C", "D", 1)])
        cost, path = dijkstra(self.graph, "A", "D")
        self.assertEqual(cost, 2)
        self.assertIn(path, [["A", "B", "D"], ["A", "C", "D"]])

    # Direction and reachability

    def testEdgesAreDirected(self):
        self.add_edges([("A", "B", 1), ("C", "A", 1)])
        # C points to A but is not reachable from A
        self.assertEqual(dijkstra(self.graph, "A", "C"), (INF, None))
        self.assertEqual(dijkstra(self.graph, "C", "B"), (2, ["C", "A", "B"]))

    def testTargetBehindStart(self):
        self.add_edges([("A", "B", 1), ("B", "C", 2)])
        self.assertEqual(dijkstra(self.graph, "B", "A"), (INF, None))

    def testDisconnectedComponent(self):
        self.add_edges([("A", "B", 1), ("X", "Y", 1)])
        self.assertEqual(dijkstra(self.graph, "A", "X"), (INF, None))
        self.assertEqual(dijkstra(self.graph, "A", "Y"), (INF, None))

    def testTargetNotInGraph(self):
        self.add_edges([("A", "B", 1)])
        self.assertEqual(dijkstra(self.graph, "A", "Z"), (INF, None))

    def testStartWithNoEdges(self):
        self.add_edges([("B", "C", 1)])
        self.assertEqual(dijkstra(self.graph, "A", "C"), (INF, None))

    # Cycles and loops

    def testCycle(self):
        self.add_edges([("A", "B", 1), ("B", "C", 1), ("C", "A", 1)])
        self.assertEqual(dijkstra(self.graph, "A", "C"), (2, ["A", "B", "C"]))

    def testCycleBackToStartDoesNotLowerStartCost(self):
        self.add_edges([("A", "B", 1), ("B", "A", 1)])
        self.assertEqual(dijkstra(self.graph, "A", "A"), (0, ["A"]))

    def testSelfLoop(self):
        self.add_edges([("A", "A", 5), ("A", "B", 1)])
        self.assertEqual(dijkstra(self.graph, "A", "B"), (1, ["A", "B"]))

    # Costs

    def testZeroCostEdges(self):
        self.add_edges([("A", "B", 0), ("B", "C", 0), ("A", "C", 1)])
        self.assertEqual(dijkstra(self.graph, "A", "C"), (0, ["A", "B", "C"]))

    def testZeroCostCycle(self):
        self.add_edges([("A", "B", 0), ("B", "C", 0), ("C", "B", 0), ("C", "D", 0)])
        self.assertEqual(dijkstra(self.graph, "A", "D"), (0, ["A", "B", "C", "D"]))

    def testFloatCosts(self):
        self.add_edges([("A", "B", 0.5), ("B", "C", 0.25), ("A", "C", 1.0)])
        cost, path = dijkstra(self.graph, "A", "C")
        self.assertAlmostEqual(cost, 0.75)
        self.assertEqual(path, ["A", "B", "C"])

    # Vertex types

    def testIntegerVertices(self):
        self.add_edges([(1, 2, 4), (1, 3, 1), (3, 2, 1), (2, 4, 1)])
        self.assertEqual(dijkstra(self.graph, 1, 4), (3, [1, 3, 2, 4]))

    def testTupleVertices(self):
        self.add_edges([((0, 0), (0, 1), 1), ((0, 1), (1, 1), 1), ((0, 0), (1, 1), 5)])
        self.assertEqual(
            dijkstra(self.graph, (0, 0), (1, 1)),
            (2, [(0, 0), (0, 1), (1, 1)]),
        )

    # Side effects

    def testDoesNotModifyGraph(self):
        self.add_edges([("A", "B", 1), ("B", "C", 2)])
        dijkstra(self.graph, "A", "C")
        self.assertEqual(self.graph.get_vertices(), {"A": {"B": 1}, "B": {"C": 2}})

    def testRepeatedCallsGiveSameResult(self):
        self.add_edges([("A", "B", 1), ("B", "C", 2), ("A", "C", 5)])
        self.assertEqual(dijkstra(self.graph, "A", "C"), dijkstra(self.graph, "A", "C"))

    # Scale

    def testLongChain(self):
        for i in range(1000):
            self.graph.add_edge(i, i + 1, 1)
        cost, path = dijkstra(self.graph, 0, 1000)
        self.assertEqual(cost, 1000)
        self.assertEqual(path, list(range(1001)))

    def testMatchesBellmanFordOnRandomGraphs(self):
        rng = random.Random(0)
        for _ in range(50):
            self.graph.clear()
            n = rng.randint(2, 15)
            edges = [
                (rng.randrange(n), rng.randrange(n), rng.randint(0, 20))
                for _ in range(rng.randint(0, 40))
            ]
            self.add_edges(edges)

            # Bellman-Ford over the final edge set (re-added edges overwrite)
            expected = {v: INF for v in range(n)}
            expected[0] = 0
            final_edges = [
                (u, v, c)
                for u, neighbours in self.graph.get_vertices().items()
                for v, c in neighbours.items()
            ]
            for _ in range(n):
                for u, v, c in final_edges:
                    if expected[u] + c < expected[v]:
                        expected[v] = expected[u] + c

            for target in range(n):
                cost, path = dijkstra(self.graph, 0, target)
                self.assertEqual(cost, expected[target], f"edges={edges}")
                if cost == INF:
                    self.assertIsNone(path)
                else:
                    # the path must be real, start and end correctly, and cost what was reported
                    self.assertEqual(path[0], 0)
                    self.assertEqual(path[-1], target)
                    self.assertEqual(self.path_cost(path), cost, f"edges={edges}")


# Sample cases from the problem page
SAMPLE_1 = [
    "###########",
    "#....T#.#.#",
    "#.#.###.#.#",
    "#.#.#.....#",
    "#.#.#.###.#",
    "#.#.#.#.#.#",
    "#.#.#.#S#.#",
    "#.#.#.#.#.#",
    "#.#.###.#.#",
    "#.........#",
    "###########",
]

SAMPLE_2 = [
    "#########",
    "#......S#",
    "#.#.#####",
    "#...#...#",
    "#.#####.#",
    "#.......#",
    "#.#####.#",
    "#.#T....#",
    "#########",
]


class TestMazeSolver(unittest.TestCase):
    def assertValidPath(self, maze, path):
        # starts at S, ends at T, moves one cell at a time and never enters a wall
        self.assertIsNotNone(path)
        self.assertEqual(maze[path[0][0]][path[0][1]], "S")
        self.assertEqual(maze[path[-1][0]][path[-1][1]], "T")
        for (a, b), (c, d) in zip(path, path[1:]):
            self.assertEqual(abs(a - c) + abs(b - d), 1, f"{(a, b)} -> {(c, d)}")
            self.assertNotEqual(maze[c][d], "#", f"walks into wall at {(c, d)}")

    def shortestLength(self, maze):
        # independent answer: number of cells on a shortest path, found by a plain
        # breadth-first search that doesn't use the solver, Graph or dijkstra
        cells = {(i, j): c for i, row in enumerate(maze) for j, c in enumerate(row)}
        start = next(p for p, c in cells.items() if c == "S")
        distance = {start: 1}
        frontier = [start]
        while frontier:
            next_frontier = []
            for i, j in frontier:
                if cells[(i, j)] == "T":
                    return distance[(i, j)]
                for p in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if cells.get(p, "#") != "#" and p not in distance:
                        distance[p] = distance[(i, j)] + 1
                        next_frontier.append(p)
            frontier = next_frontier
        return float("inf")

    # Samples

    def testSample1(self):
        path = solve_maze(SAMPLE_1)
        self.assertValidPath(SAMPLE_1, path)
        self.assertEqual(len(path), 18)

    def testSample2(self):
        # two routes of equal length exist, so only check validity and length
        path = solve_maze(SAMPLE_2)
        self.assertValidPath(SAMPLE_2, path)
        self.assertEqual(len(path), 23)

    # Small mazes with one exact answer

    def testStartNextToTarget(self):
        self.assertEqual(solve_maze(["ST"]), [(0, 0), (0, 1)])

    def testTargetAboveStart(self):
        self.assertEqual(solve_maze(["T", "S"]), [(1, 0), (0, 0)])

    def testStraightCorridor(self):
        self.assertEqual(
            solve_maze(["#####", "#S.T#", "#####"]),
            [(1, 1), (1, 2), (1, 3)],
        )

    def testWindingCorridor(self):
        maze = [
            "#####",
            "#S#T#",
            "#.#.#",
            "#...#",
            "#####",
        ]
        self.assertEqual(
            solve_maze(maze),
            [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3)],
        )

    def testAvoidsDeadEnd(self):
        maze = [
            "#######",
            "#S....#",
            "#.###.#",
            "#.#T..#",
            "#######",
        ]
        self.assertEqual(
            solve_maze(maze),
            [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3)],
        )

    # Choosing a short path

    def testOpenGridGivesShortestPath(self):
        # with no walls the path must be a straight-line distance long
        maze = ["S....", ".....", ".....", "....T"]
        path = solve_maze(maze)
        self.assertValidPath(maze, path)
        self.assertEqual(len(path), 3 + 4 + 1)

    def testShortRouteBeatsLongRoute(self):
        maze = [
            "S.T",
            ".#.",
            "...",
        ]
        self.assertEqual(solve_maze(maze), [(0, 0), (0, 1), (0, 2)])

    # Grid edges and shapes

    def testNoBorderWalls(self):
        # S and T in the corners, so neighbours outside the grid must be ignored
        maze = ["S..", "##.", "T.."]
        self.assertEqual(
            solve_maze(maze),
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)],
        )

    def testSingleColumn(self):
        maze = ["S", ".", ".", "T"]
        self.assertEqual(solve_maze(maze), [(0, 0), (1, 0), (2, 0), (3, 0)])

    def testNonSquareMaze(self):
        maze = ["S.........", "#########.", "T........."]
        path = solve_maze(maze)
        self.assertValidPath(maze, path)
        self.assertEqual(len(path), 21)

    # No path

    def testTargetWalledOff(self):
        self.assertIsNone(solve_maze(["S#T"]))

    def testMissingTarget(self):
        self.assertIsNone(solve_maze(["S.."]))

    def testMissingStart(self):
        self.assertIsNone(solve_maze(["..T"]))

    # Scale and cross-checking

    def testRandomMazesMatchDijkstra(self):
        rng = random.Random(0)
        for _ in range(100):
            n, m = rng.randint(1, 12), rng.randint(2, 12)
            maze = [["." if rng.random() < 0.7 else "#" for _ in range(m)] for _ in range(n)]
            cells = rng.sample([(i, j) for i in range(n) for j in range(m)], 2)
            (si, sj), (ti, tj) = cells
            maze[si][sj], maze[ti][tj] = "S", "T"
            maze = ["".join(row) for row in maze]

            path = solve_maze(maze)
            expected = self.shortestLength(maze)
            if expected == float("inf"):
                self.assertIsNone(path, maze)
            else:
                self.assertValidPath(maze, path)
                self.assertEqual(len(path), expected, maze)

    def testLargestMaze(self):
        # 1000 x 1000 with no walls: path runs corner to corner
        maze = ["S" + "." * 999] + ["." * 1000] * 998 + ["." * 999 + "T"]
        path = solve_maze(maze)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (999, 999))
        self.assertEqual(len(path), 1999)


if __name__ == "__main__":
    unittest.main(verbosity=2)
