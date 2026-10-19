import os
import random
import tempfile
import time
import unittest
from collections.abc import Callable, Sequence

from sequence_alignment import (
    GAP,
    MATCH,
    MISMATCH,
    match_score,
    read_kotlin,
    score_matrix,
    show_alignment,
    smith_waterman,
)
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


class TestSequenceAlignment(unittest.TestCase):
    def testMatchScore(self):
        self.assertEqual(match_score("A", "A"), MATCH)
        self.assertEqual(match_score("A", "C"), MISMATCH)

    def testScoreMatrixShape(self):
        H = score_matrix("ACG", "ACGTT")
        self.assertEqual(len(H), 4)
        self.assertEqual(len(H[0]), 6)

    def testScoreMatrixFirstRowAndColumnAreZero(self):
        H = score_matrix("TGTTACGG", "GGTTGACTA")
        self.assertEqual(H[0], [0] * 10)
        self.assertEqual([row[0] for row in H], [0] * 9)

    def testScoreMatrixNeverNegative(self):
        H = score_matrix("AAAACCCC", "GGGGTTTT")
        for row in H:
            for value in row:
                self.assertGreaterEqual(value, 0)

    def testScoreMatrixWikipedia(self):
        # Example table from the Smith-Waterman Wikipedia page
        H = score_matrix("TGTTACGG", "GGTTGACTA")
        self.assertEqual(H[1], [0, 0, 0, 3, 3, 1, 0, 0, 3, 1])
        self.assertEqual(H[6][7], 13)

    def testWikipediaExample(self):
        self.assertEqual(smith_waterman("TGTTACGG", "GGTTGACTA"), (13, "GTT-AC", "GTTGAC"))

    def testIdenticalSequences(self):
        self.assertEqual(smith_waterman("ACGTACGT", "ACGTACGT"), (8 * MATCH, "ACGTACGT", "ACGTACGT"))

    def testNoMatch(self):
        self.assertEqual(smith_waterman("AAAA", "CCCC"), (0, "", ""))

    def testEmptySequence(self):
        self.assertEqual(smith_waterman("", "ACGT"), (0, "", ""))
        self.assertEqual(smith_waterman("ACGT", ""), (0, "", ""))

    def testFindsSubstring(self):
        # a local alignment ignores the unrelated ends of the longer sequence
        self.assertEqual(smith_waterman("GATTACA", "CCCCGATTACACCCC"), (7 * MATCH, "GATTACA", "GATTACA"))

    def testFindsSubstringInRandomDNA(self):
        random.seed(1)
        query = "".join(random.choice("ACGT") for _ in range(40))
        left = "".join(random.choice("ACGT") for _ in range(200))
        right = "".join(random.choice("ACGT") for _ in range(200))
        score, aligned_query, aligned_target = smith_waterman(query, left + query + right)
        self.assertEqual(score, 40 * MATCH)
        self.assertEqual(aligned_query, query)
        self.assertEqual(aligned_target, query)

    def testGapInFirstSequence(self):
        self.assertEqual(smith_waterman("ACGTTGCA", "ACGTATGCA"), (8 * MATCH + GAP, "ACGT-TGCA", "ACGTATGCA"))

    def testGapInSecondSequence(self):
        self.assertEqual(smith_waterman("ACGTATGCA", "ACGTTGCA"), (8 * MATCH + GAP, "ACGTATGCA", "ACGT-TGCA"))

    def testMismatchInMiddle(self):
        self.assertEqual(smith_waterman("ACGTCAGT", "ACGTGAGT"), (7 * MATCH + MISMATCH, "ACGTCAGT", "ACGTGAGT"))

    def testAlignedStringsSameLength(self):
        _, aligned_a, aligned_b = smith_waterman("TTGACACCCTCCCAATTGTA", "ACCCCAGGCTTTACACAGGAAC")
        self.assertEqual(len(aligned_a), len(aligned_b))

    def testAlignmentScoreMatchesReturnedScore(self):
        # rescoring the returned alignment column by column gives the same score
        score, aligned_a, aligned_b = smith_waterman("TTGACACCCTCCCAATTGTA", "ACCCCAGGCTTTACACAGGAAC")
        total = 0
        for x, y in zip(aligned_a, aligned_b):
            if x == "-" or y == "-":
                total += GAP
            else:
                total += match_score(x, y)
        self.assertEqual(total, score)

    def testAlignedPartsComeFromInputs(self):
        a = "TTGACACCCTCCCAATTGTA"
        b = "ACCCCAGGCTTTACACAGGAAC"
        _, aligned_a, aligned_b = smith_waterman(a, b)
        self.assertIn(aligned_a.replace("-", ""), a)
        self.assertIn(aligned_b.replace("-", ""), b)

    def testShowAlignment(self):
        self.assertEqual(show_alignment("GTT-AC", "GTTGAC"), "GTT-AC\n||| ||\nGTTGAC\n")

    def testShowAlignmentWrapsRows(self):
        text = show_alignment("AAAA", "AAAA", width=2)
        self.assertEqual(text, "AA\n||\nAA\n\nAA\n||\nAA\n")

    def testReadKotlin(self):
        with tempfile.NamedTemporaryFile("w", suffix=".kt", delete=False) as f:
            f.write('// comment\nval genomeSnippet = "ACGT"\nval testAgainst = "GGTT"\n')
        try:
            self.assertEqual(read_kotlin(f.name), {"genomeSnippet": "ACGT", "testAgainst": "GGTT"})
        finally:
            os.remove(f.name)

    def testGenomeMatchesSnippet(self):
        # testAgainst should line up with the part of targetGenome holding genomeSnippet
        seqs = read_kotlin(os.path.join(os.path.dirname(__file__), "Genome.kt"))
        _, _, aligned_target = smith_waterman(seqs["testAgainst"], seqs["targetGenome"])
        self.assertEqual(aligned_target.replace("-", ""), seqs["genomeSnippet"])


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
