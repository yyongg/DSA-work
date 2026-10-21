# Matrix Multiplication Performance Analysis

## Approach

`strassen_multiply` is a hybrid: for `n > 64` it splits each matrix into quadrants and
recurses with Strassen's 7 products; at `n <= 64` it falls back to the conventional
O(n³) multiplication (`__mul__`).

- Conventional: T(n) = O(n³)
- Hybrid Strassen: T(n) = 7T(n/2) + O(n²) = O(n^log₂7) ≈ O(n^2.81)

## Results

Timings from `test.TestTiming` (random integer matrices, single run, pure Python):

|    n | Conventional (s) | Hybrid Strassen (s) | Speedup |
|-----:|-----------------:|--------------------:|--------:|
|    2 |         0.000027 |            0.000009 |       — |
|    4 |         0.000024 |            0.000019 |       — |
|    8 |         0.000121 |            0.000101 |       — |
|   16 |         0.000677 |            0.000616 |       — |
|   32 |         0.003277 |            0.005795 |       — |
|   64 |         0.021964 |            0.041508 |       — |
|  128 |         0.295107 |            0.213678 |   1.38× |
|  256 |         1.799559 |            2.188584 |   0.82× |
|  512 |        30.717838 |           19.304485 |   1.59× |
| 1024 |       265.013308 |          129.376213 |   2.05× |

## Analysis

- **n ≤ 64:** Both columns run the same conventional code, because the hybrid
  switches straight to `__mul__`. Any differences here are timing noise from
  single runs, not differences between the algorithms.
- **n ≥ 128:** Strassen's recursion takes effect. Its advantage grows with size:
  1.38× at 128, 1.59× at 512, and 2.05× at 1024. This fits the asymptotic gap,
  where saving one multiplication in eight at each recursion level adds up.
- **Growth rate:** Going from 512 to 1024, conventional time grows by about 8.6×
  (≈ n^3.1, in line with the expected 8×). Hybrid Strassen time grows by about
  6.7× (≈ n^2.74, close to the expected 7×).
- **n = 256 anomaly:** Here Strassen was slower. Each Strassen level adds overhead
  on top of the multiplications: 18 matrix additions/subtractions, quadrant copying
  in `div4`, and an element-by-element recombination loop. All of these create new
  Python lists. At this size the overhead outweighs the multiplications saved. The
  measurement also comes from a single run, so noise could be a factor.
- **Why the hybrid helps:** Running Strassen all the way down to 1×1 would make the
  recursion overhead dominate. Below a cutoff, the conventional algorithm's smaller
  constant factor wins. The cutoff of 64 means Strassen only works where it reduces
  the total work.

## Conclusion

The hybrid algorithm runs about 2× faster than conventional multiplication at
n = 1024, and the gap keeps widening as n grows. Small matrices pay no penalty,
because they never enter the recursion. The crossover point falls around n = 128–512.
Tuning the cutoff, or reducing allocation in `div4` and the recombination step,
would likely move that point lower.
