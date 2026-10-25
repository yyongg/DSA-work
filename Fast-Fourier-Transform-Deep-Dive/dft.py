"""Implementation of discrete fourier transform"""

import cmath

def dft_coefficient(x_vals: list[float], k: int) -> tuple[float,float]:
    """Compute the k-th DFT coefficient of a real-valued signal.

    Evaluates X_k = sum_{n=0}^{N-1} x_n * e^{-2*pi*i*k*n/N}.

    Args:
        x_vals: Samples x_0, ..., x_{N-1} of the signal.
        k: Index of the frequency bin to compute, typically 0 <= k < N.

    Returns:
        The coefficient X_k as a (real, imaginary) tuple.
    """
    total: complex = 0
    N:int = len(x_vals)
    for i, x in enumerate(x_vals):
        total += cmath.rect(x, -1*2*cmath.pi*k*i/N)
    return (total.real, total.imag)

def dft(x_vals: list[float]) -> list[tuple[float,float]]:
    """Compute the discrete Fourier transform of a real-valued signal.

    Directly evaluates every coefficient, taking O(N^2) time.

    Args:
        x_vals: Samples x_0, ..., x_{N-1} of the signal.

    Returns:
        A list of N coefficients X_0, ..., X_{N-1}, each as a
        (real, imaginary) tuple. Returns an empty list for empty input.
    """
    N: int = len(x_vals)
    return [dft_coefficient(x_vals, i) for i in range(N)]
