# Assignment 8 – K-D Tree

## Implementation

To build the tree, the points are sorted on one axis at each level (cycling through `0, 1, ..., k-1`), and the median point becomes the node. This keeps the tree balanced, with a depth of about log2(n).

To find the nearest neighbor, the search first goes down the side of each splitting plane that the query is on. It only searches the other side if the plane is closer to the query than the best point found so far; otherwise, that whole subtree is skipped. The brute force search simply computes the distance from the query to every point and keeps the smallest. Both compare squared distances, which gives the same ordering as Euclidean distance without needing a square root.

## Experiment setup

An experiment was run for each combination of `k` in {1, 2, 3, 5, 10, 20} and `numPoints` in {10, 100, 1,000, 10,000}. For each one, `run_experiment` generates `numPoints` random training points and 1,000 random test points, with every coordinate uniform in [0, 1). It then times three things: building the tree, finding the nearest neighbor of all 1,000 test points with the tree, and finding the nearest neighbor of the same 1,000 test points with brute force.

Python has no `Duration` type, so `run_experiment` returns the three times as floats in seconds. The random seed is fixed at 0, so the data is the same on every run. The times are from a single run of pure Python on one laptop, so treat small differences as noise.

## Results

### Raw times (seconds, 1,000 queries)

| k | numPoints | Build | K-D tree query | Brute force | Speedup |
|---|---|---|---|---|---|
| 1 | 10 | 0.0001 | 0.0027 | 0.0039 | 1.4x |
| 1 | 100 | 0.0002 | 0.0062 | 0.0276 | 4.4x |
| 1 | 1,000 | 0.0025 | 0.0067 | 0.2294 | 34.2x |
| 1 | 10,000 | 0.0227 | 0.0040 | 1.4891 | 370.3x |
| 2 | 10 | 0.0000 | 0.0026 | 0.0022 | 0.8x |
| 2 | 100 | 0.0001 | 0.0039 | 0.0185 | 4.7x |
| 2 | 1,000 | 0.0012 | 0.0053 | 0.2198 | 41.1x |
| 2 | 10,000 | 0.0426 | 0.0098 | 5.2952 | 540.6x |
| 3 | 10 | 0.0002 | 0.0082 | 0.0089 | 1.1x |
| 3 | 100 | 0.0003 | 0.0180 | 0.0635 | 3.5x |
| 3 | 1,000 | 0.0039 | 0.0292 | 0.7354 | 25.2x |
| 3 | 10,000 | 0.0591 | 0.0506 | 6.0727 | 120.0x |
| 5 | 10 | 0.0001 | 0.0108 | 0.0052 | 0.5x |
| 5 | 100 | 0.0005 | 0.0500 | 0.0816 | 1.6x |
| 5 | 1,000 | 0.0030 | 0.0957 | 1.0036 | 10.5x |
| 5 | 10,000 | 0.0418 | 0.1464 | 9.6655 | 66.0x |
| 10 | 10 | 0.0001 | 0.0164 | 0.0107 | 0.7x |
| 10 | 100 | 0.0010 | 0.1258 | 0.0875 | 0.7x |
| 10 | 1,000 | 0.0030 | 0.9885 | 1.1632 | 1.2x |
| 10 | 10,000 | 0.0373 | 5.6439 | 16.7873 | 3.0x |
| 20 | 10 | 0.0000 | 0.0303 | 0.0326 | 1.1x |
| 20 | 100 | 0.0003 | 0.3515 | 0.3168 | 0.9x |
| 20 | 1,000 | 0.0031 | 3.5487 | 3.2101 | 0.9x |
| 20 | 10,000 | 0.0597 | 42.0437 | 31.2795 | 0.7x |

Speedup = brute force time / K-D tree query time. A value above 1x means the tree was faster.

### Speedup summary

| k \ numPoints | 10 | 100 | 1,000 | 10,000 |
|---|---|---|---|---|
| **1** | 1.4x | 4.4x | 34.2x | **370.3x** |
| **2** | 0.8x | 4.7x | 41.1x | **540.6x** |
| **3** | 1.1x | 3.5x | 25.2x | **120.0x** |
| **5** | 0.5x | 1.6x | 10.5x | **66.0x** |
| **10** | 0.7x | 0.7x | 1.2x | 3.0x |
| **20** | 1.1x | 0.9x | 0.9x | 0.7x |

## Observations

Brute force time grows linearly with `numPoints`. Every query looks at every point, so 10x more points means about 10x more time; for example, at k = 5 it took 0.08 s, then 1.0 s, then 9.7 s. In low dimensions, the K-D tree's query time barely grows at all. For k ≤ 3, going from 1,000 to 10,000 points changed the tree's query time very little, because each query only visits about log(n) nodes plus a few neighbors. Building the tree was also cheap: even at 10,000 points it took under 0.06 s. That is less than 1% of the brute force time and is paid only once, so it does not change any of the conclusions.

The tree's advantage disappears as `k` grows. At k = 10 the tree is only 3x faster even with 10,000 points, and at k = 20 it is *slower* than brute force at every size. In high dimensions, the distance to the nearest neighbor is large compared to the distance to most splitting planes. As a result, the `diff² < best` check almost never lets the search skip a subtree, so the tree ends up visiting nearly every node and pays for the recursion on top of that. With very few points (10), the two methods are about even. There is too little data to skip, so the speedup ranges from 0.5x to 1.4x, depending mostly on overhead.

## When K-D trees beat brute force

K-D trees are most effective when the dimension is low. The tree was 25x to 540x faster for k ≤ 3 at 1,000 or more points, and still 66x faster at k = 5. A common rule of thumb is that the tree only helps when `numPoints` is much larger than 2^k. This matches the data: at k = 10 (2^10 ≈ 1,000) the tree only starts to pull ahead at 10,000 points, and at k = 20 (2^20 ≈ 1,000,000) none of the dataset sizes were large enough.

K-D trees also do better as the number of points grows, since the tree's query cost grows roughly like log(n) while brute force grows like n. Finally, they are worth it when the same data is queried many times. Building the tree is a one-time cost, and it was always small compared to running 1,000 queries.

Brute force is the better choice for high-dimensional data (around k ≥ 10 at these sizes) or for very small datasets. In those cases the tree cannot skip enough of the data to make up for its extra overhead, and brute force is also simpler.
