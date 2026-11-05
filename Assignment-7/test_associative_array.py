"""Unit tests for AssociativeArray"""

import unittest
from associative_array import AssociativeArray


class TestAssociativeArray(unittest.TestCase):
    def setUp(self):
        self.a = AssociativeArray()

    def test_set_and_get(self):
        self.a["x"] = 1
        self.assertEqual(self.a["x"], 1)

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.a["missing"])

    def test_overwrite(self):
        self.a["x"] = 1
        self.a["x"] = 2
        self.assertEqual(self.a["x"], 2)
        self.assertEqual(len(self.a), 1)

    def test_contains(self):
        self.a["x"] = 1
        self.assertIn("x", self.a)
        self.assertNotIn("y", self.a)

    def test_remove(self):
        self.a["x"] = 1
        self.assertTrue(self.a.remove("x"))
        self.assertNotIn("x", self.a)
        self.assertFalse(self.a.remove("x"))

    def test_len(self):
        self.assertEqual(len(self.a), 0)
        self.a["x"] = 1
        self.a["y"] = 2
        self.assertEqual(len(self.a), 2)

    def test_key_value_pairs(self):
        self.a["x"] = 1
        self.a["y"] = 2
        self.assertCountEqual(self.a.key_value_pairs(), [("x", 1), ("y", 2)])

    def test_grows_past_initial_length(self):
        a = AssociativeArray(initial_length=2)
        for i in range(20):
            a[i] = i * 10
        self.assertEqual(len(a), 20)
        self.assertTrue(all(a[i] == i * 10 for i in range(20)))


if __name__ == "__main__":
    unittest.main()
