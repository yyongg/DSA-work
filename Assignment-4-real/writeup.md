# Sorting Algorithm Runtimes

## Method

- Tests: `better_tests.py`
- List sizes: 100, 500, 1000, 2000, 5000
- Lists: random integers from 1 to 100,000
- Each size was run 5 times, with a new random list each time. All four algorithms sorted a copy of the same list.
- Timing: `time.perf_counter()` around each sort call. The table shows the average of the 5 runs.
- Each result was checked against Python's `sorted()`.

## Results (average ms)

| Size | Quick Sort | Check All | Merge Sort | Insertion Sort |
|---|---|---|---|---|
| 100 | 0.07 | 0.12 | 0.12 | 0.15 |
| 500 | 0.37 | 2.50 | 0.76 | 3.46 |
| 1000 | 0.85 | 11.72 | 2.09 | 17.51 |
| 2000 | 2.10 | 43.60 | 4.14 | 66.00 |
| 5000 | 4.81 | 243.13 | 10.17 | 400.06 |

## Conclusions

At small sizes (100 elements), all four algorithms finished in under 0.2 ms, so the choice of algorithm barely matters for short lists. As the lists grew, the algorithms split into two groups. Check All and Insertion Sort behaved like O(n²): when the size doubled, their times roughly quadrupled (for example, Insertion Sort went from 17.51 ms to 66.00 ms), and at 5000 elements they were 50–80x slower than Quick Sort. Insertion Sort was the slowest on random lists because it shifts elements one position at a time, so each new element moves past about half of the already-sorted part on average. On an already-sorted or nearly sorted list, though, it would run close to O(n) and be much faster.

Quick Sort and Merge Sort grew at about O(n log n), with times rising only slightly faster than the list size. Quick Sort was the fastest at every size, about twice as fast as Merge Sort, because Merge Sort spends extra time slicing lists and building new ones during each merge. One caveat is that all the test lists were random. Quick Sort uses the last element as its pivot, so on an already-sorted list it would slow down to O(n²) and could hit Python's recursion limit, while Merge Sort stays O(n log n) for any input. Overall, Quick Sort is the best choice for random data, Merge Sort is the safer choice when the input order is unknown, and the O(n²) algorithms are only reasonable for small or nearly sorted lists.
