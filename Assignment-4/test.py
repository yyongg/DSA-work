import random
import time
import unittest
from collections.abc import Callable, Sequence

from square_matrix import SquareMatrix


def make_matrix(rows: Sequence[Sequence[float]]) -> SquareMatrix:
    """Build a SquareMatrix from a list of rows."""
    mat = SquareMatrix()
    mat.zeros(len(rows))
    for i, row in enumerate(rows):
        for j, elem in enumerate(row):
            mat.set_elem(i, j, elem)
    return mat


def random_matrix(n: int) -> SquareMatrix:
    """Build an n x n matrix of random integers from -10 to 10."""
    return make_matrix([[random.randint(-10, 10) for _ in range(n)] for _ in range(n)])


def to_rows(mat: SquareMatrix) -> list[list[float]]:
    """Copy a SquareMatrix out into a list of rows."""
    return [[mat.get_elem(i, j) for j in range(mat.size)] for i in range(mat.size)]


class TestSquareMatrix(unittest.TestCase):
    def setUp(self) -> None:
        self.a = make_matrix([[1, 2], [3, 4]])
        self.b = make_matrix([[5, 6], [7, 8]])

    def testZeros(self):
        mat = SquareMatrix()
        mat.zeros(4)
        self.assertEqual(mat.size, 4)
        self.assertEqual(to_rows(mat), [[0] * 4 for _ in range(4)])

    def testSetAndGet(self):
        self.a.set_elem(0, 1, 9)
        self.assertEqual(self.a.get_elem(0, 1), 9)
        self.assertEqual(self.a.get_row(0), [1, 9])
        self.assertEqual(self.a.get_col(1), [9, 4])

    def testAdd(self):
        self.assertEqual(to_rows(self.a + self.b), [[6, 8], [10, 12]])

    def testSub(self):
        self.assertEqual(to_rows(self.b - self.a), [[4, 4], [4, 4]])

    def testDiv4(self):
        mat = make_matrix([[4 * i + j for j in range(4)] for i in range(4)])
        tl, tr, bl, br = mat.div4()
        self.assertEqual(to_rows(tl), [[0, 1], [4, 5]])
        self.assertEqual(to_rows(tr), [[2, 3], [6, 7]])
        self.assertEqual(to_rows(bl), [[8, 9], [12, 13]])
        self.assertEqual(to_rows(br), [[10, 11], [14, 15]])

    def testMul(self):
        self.assertEqual(to_rows(self.a * self.b), [[19, 22], [43, 50]])

    def testDifferentSizesRaise(self):
        big = random_matrix(4)
        with self.assertRaises(ValueError):
            _ = self.a + big
        with self.assertRaises(ValueError):
            _ = self.a - big
        with self.assertRaises(ValueError):
            _ = self.a * big


class TestStrassen(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(0)

    def testStrassen1x1(self):
        result = make_matrix([[3]]).strassen_multiply(make_matrix([[4]]))
        self.assertEqual(to_rows(result), [[12]])

    def testStrassen2x2(self):
        a = make_matrix([[1, 2], [3, 4]])
        b = make_matrix([[5, 6], [7, 8]])
        self.assertEqual(to_rows(a.strassen_multiply(b)), [[19, 22], [43, 50]])

    def testMatchesRegularMultiplication(self):
        for n in [4, 8, 16, 32, 64, 128]:
            with self.subTest(n=n):
                a = random_matrix(n)
                b = random_matrix(n)
                self.assertEqual(to_rows(a.strassen_multiply(b)), to_rows(a * b))

    def testDifferentSizesRaise(self):
        with self.assertRaises(ValueError):
            random_matrix(2).strassen_multiply(random_matrix(4))


class TestTiming(unittest.TestCase):
    def time_call(self, func: Callable[[], object]) -> float:
        """Return how long func() takes, in seconds."""
        start = time.perf_counter()
        func()
        return time.perf_counter() - start

    def testCompareSmallAndBigMatrices(self):
        random.seed(0)
        print("\n\n   n |   regular (s) |  strassen (s)")
        print("-----+---------------+--------------")
        for n in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
            a = random_matrix(n)
            b = random_matrix(n)
            regular = self.time_call(lambda: a * b)
            strassen = self.time_call(lambda: a.strassen_multiply(b))
            print(f"{n:4} | {regular:13.6f} | {strassen:13.6f}")


if __name__ == "__main__":
    unittest.main()
