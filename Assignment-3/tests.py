import unittest

from graph import Graph


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
