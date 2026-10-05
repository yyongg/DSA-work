"""Runtime benchmark for sorting algorithms"""

import random
import time
from sort_algorithms import quick_sort, check_all, merge_sort, insertion_sort

SIZES = [100, 500, 1000, 2000, 5000]
TRIALS = 5
ALGORITHMS = {
    "Quick Sort": quick_sort,
    "Check All": check_all,
    "Merge Sort": merge_sort,
    "Insertion Sort": insertion_sort,
}

print("| Size | " + " | ".join(ALGORITHMS) + " |")
print("|---" * (len(ALGORITHMS) + 1) + "|")

for size in SIZES:
    totals = {name: 0.0 for name in ALGORITHMS}

    for _ in range(TRIALS):
        arr = [random.randint(1, 100_000) for _ in range(size)]
        for name, sort in ALGORITHMS.items():
            data = arr.copy()  # check_all and insertion_sort mutate their input
            start = time.perf_counter()
            res = sort(data)
            totals[name] += time.perf_counter() - start
            assert res == sorted(arr), f"{name} failed"

    row = " | ".join(f"{totals[name] / TRIALS * 1000:.2f}" for name in ALGORITHMS)
    print(f"| {size} | {row} |")
