"""Plot the DFT vs. FFT timings in benchmark_results.csv (measured with test.py)."""

import csv

import matplotlib.pyplot as plt

with open("benchmark_results.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

ns = [int(row["n"]) for row in rows]
dft_times = [float(row["dft_seconds"]) for row in rows]
fft_times = [float(row["fft_seconds"]) for row in rows]

plt.figure(figsize=(8, 5))
plt.plot(ns, dft_times, marker="o", color="#2a78d6", label="DFT  O(N²)")
plt.plot(ns, fft_times, marker="o", color="#eb6834", label="FFT  O(N log N)")
plt.xscale("log", base=2)
plt.yscale("log")
plt.xlabel("Input size N")
plt.ylabel("Runtime (seconds, log scale)")
plt.title("DFT vs. FFT runtime")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("benchmark.png", dpi=150)
