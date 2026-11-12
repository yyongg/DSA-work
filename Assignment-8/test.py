"""Unit tests for KDTree and brute force nearest neighbor"""

import random
import unittest
from kd_tree import KDTree, brute_force_nearest, squared_distance


class TestBruteForce(unittest.TestCase):
    def test_simple(self):
        points = [(0, 0), (10, 10), (3, 3), (-5, 2)]
        self.assertEqual(brute_force_nearest(points, (4, 4)), (3, 3))

    def test_exact_match(self):
        points = [(0, 0), (1, 2), (7, 7)]
        self.assertEqual(brute_force_nearest(points, (1, 2)), (1, 2))


class TestKDTree(unittest.TestCase):
    def test_root_is_median(self):
        tree = KDTree([(1, 0), (5, 0), (3, 0)])
        assert tree.root is not None
        self.assertEqual(tree.root.point, (3, 0))

    def test_single_point(self):
        tree = KDTree([(2, 3)])
        self.assertEqual(tree.nearest((100, -100)), (2, 3))

    def test_small_example(self):
        tree = KDTree([(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)])
        self.assertEqual(tree.nearest((9, 2)), (8, 1))
        self.assertEqual(tree.nearest((1, 1)), (2, 3))
        self.assertEqual(tree.nearest((4, 8)), (4, 7))

    def test_exact_match(self):
        points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
        tree = KDTree(points)
        for p in points:
            self.assertEqual(tree.nearest(p), p)

    def test_answer_across_split(self):
        """Query lands right of the root's split (x=5) but the answer is on the left"""
        tree = KDTree([(4.9, 0), (5, 50), (6, 50), (7, 50)])
        self.assertEqual(tree.nearest((5.1, 0)), (4.9, 0))

    def test_1d(self):
        tree = KDTree([(1,), (10,), (5,), (7,), (-3,)])
        self.assertEqual(tree.nearest((8.9,)), (10,))
        self.assertEqual(tree.nearest((-100,)), (-3,))

    def test_matches_brute_force(self):
        """Random points in several dimensions; compare distances in case of ties"""
        rng = random.Random(42)
        for k in (1, 2, 3, 5, 10):
            for n in (1, 10, 100, 1000):
                points = [tuple(rng.random() for _ in range(k)) for _ in range(n)]
                tree = KDTree(points)
                for _ in range(50):
                    q = tuple(rng.random() for _ in range(k))
                    self.assertEqual(squared_distance(tree.nearest(q), q),
                                     squared_distance(brute_force_nearest(points, q), q))


if __name__ == "__main__":
    unittest.main()
