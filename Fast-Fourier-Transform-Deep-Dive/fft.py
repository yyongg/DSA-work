"""Implementation of fast fourier transform (recursive radix-2 Cooley-Tukey)"""

import cmath

def _fft_recursive(x_vals: list[complex]) -> list[complex]:
    """Recursively compute the DFT of a signal whose length is a power of 2.

    Splits the signal into even- and odd-indexed samples, transforms each
    half, then combines them with the butterfly step:
        X_k         = E_k + w^k * O_k
        X_{k + N/2} = E_k - w^k * O_k
    where w = e^{-2*pi*i/N}.

    Args:
        x_vals: Samples x_0, ..., x_{N-1}, with N a power of 2.

    Returns:
        The coefficients X_0, ..., X_{N-1} as complex numbers.
    """
    N: int = len(x_vals)
    if N == 1:
        return [x_vals[0]]

    evens: list[complex] = _fft_recursive(x_vals[0::2])
    odds: list[complex] = _fft_recursive(x_vals[1::2])

    result: list[complex] = [0] * N
    for k in range(N // 2):
        twiddle: complex = cmath.rect(1, -2*cmath.pi*k/N) * odds[k]
        result[k] = evens[k] + twiddle
        result[k + N//2] = evens[k] - twiddle
    return result

def fft(x_vals: list[float]) -> list[tuple[float,float]]:
    """Compute the discrete Fourier transform of a real-valued signal.

    Uses the recursive radix-2 Cooley-Tukey algorithm, taking O(N log N) time.
    Produces the same output as dft.dft.

    Args:
        x_vals: Samples x_0, ..., x_{N-1} of the signal. N must be a power of 2.

    Returns:
        A list of N coefficients X_0, ..., X_{N-1}, each as a
        (real, imaginary) tuple. Returns an empty list for empty input.

    Raises:
        ValueError: If N is not a power of 2.
    """
    N: int = len(x_vals)
    if N == 0:
        return []
    if N & (N - 1) != 0:
        raise ValueError(f"Input length must be a power of 2, got {N}")
    return [(X.real, X.imag) for X in _fft_recursive([complex(x) for x in x_vals])]
