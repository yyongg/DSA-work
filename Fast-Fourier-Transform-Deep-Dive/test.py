import math
import random
import timeit
import unittest

from dft import dft
from fft import fft


def random_signal(n: int) -> list[float]:
    return [random.uniform(-10, 10) for _ in range(n)]


def best_time(func, x_vals: list[float], repeats: int) -> float:
    """Return the fastest of several runs of func(x_vals), in seconds."""
    return min(timeit.repeat(lambda: func(x_vals), number=1, repeat=repeats))


class TestCorrectness(unittest.TestCase):
    def assertTransformsClose(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for (er, ei), (ar, ai) in zip(expected, actual):
            self.assertTrue(math.isclose(er, ar, abs_tol=1e-9))
            self.assertTrue(math.isclose(ei, ai, abs_tol=1e-9))

    def testEmptyInput(self):
        self.assertEqual(dft([]), [])
        self.assertEqual(fft([]), [])

    def testSingleSample(self):
        self.assertTransformsClose(dft([3.0]), [(3.0, 0.0)])
        self.assertTransformsClose(fft([3.0]), [(3.0, 0.0)])

    def testImpulseIsFlat(self):
        # The DFT of [1, 0, 0, ...] is 1 in every bin
        x = [1.0] + [0.0] * 7
        self.assertTransformsClose(fft(x), [(1.0, 0.0)] * 8)

    def testConstantIsAllInBinZero(self):
        x = [2.0] * 8
        self.assertTransformsClose(fft(x), [(16.0, 0.0)] + [(0.0, 0.0)] * 7)

    def testFftMatchesDft(self):
        for n in [1, 2, 4, 8, 16, 64, 256]:
            x = random_signal(n)
            self.assertTransformsClose(dft(x), fft(x))

    def testFftRejectsNonPowerOfTwo(self):
        for n in [3, 5, 6, 12]:
            with self.assertRaises(ValueError):
                fft(random_signal(n))


class TestSpeed(unittest.TestCase):
    SIZES = [2 ** p for p in range(4, 16)]  # 16 to 32768
    REPEATS = 3

    def testCompareSpeed(self):
        print(f"\n{'N':>6} | {'DFT (s)':>10} | {'FFT (s)':>10} | {'speedup':>8}")
        print("-" * 44)
        for n in self.SIZES:
            x = random_signal(n)
            dft_time = best_time(dft, x, self.REPEATS)
            fft_time = best_time(fft, x, self.REPEATS)
            print(f"{n:>6} | {dft_time:>10.6f} | {fft_time:>10.6f} | {dft_time / fft_time:>7.1f}x")

            # At small N the FFT's recursion overhead can outweigh its
            # better complexity, so only require it to win for larger inputs
            if n >= 256:
                self.assertLess(fft_time, dft_time)


if __name__ == "__main__":
    unittest.main(verbosity=2)
