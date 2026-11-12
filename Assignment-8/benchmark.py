"""Benchmark KDTree against brute force nearest neighbor search."""

import random
import time

from kd_tree import KDTree, Point, brute_force_nearest

NUM_TEST_POINTS = 1000


def random_point(k: int) -> Point:
    """Creates a random k-dimensional point with coordinates in [0, 1).

    Args:
        k: The dimension of the point.

    Returns:
        The random point.
    """

    coords: list[float] = []
    for _ in range(k):
        coords.append(random.random())
    return tuple(coords)


def random_points(k: int, n: int) -> list[Point]:
    """Creates a list of random k-dimensional points.

    Args:
        k: The dimension of each point.
        n: The number of points.

    Returns:
        The list of random points.
    """

    points: list[Point] = []
    for _ in range(n):
        points.append(random_point(k))
    return points


def run_experiment(k: int, num_points: int) -> tuple[float, float, float]:
    """Benchmarks KDTree against brute force nearest neighbor.

    1000 test points are generated to test against the training points.

    Args:
        k: The dimensionality of the dataset to create.
        num_points: The number of points to match against.

    Returns:
        A triple of times in seconds: the time to build the tree, the time to
        query the tree with 1000 points, and the time to find the nearest
        neighbor of those 1000 points using brute force.
    """

    train = random_points(k, num_points)
    test = random_points(k, NUM_TEST_POINTS)

    start = time.perf_counter()
    tree = KDTree(train)
    build_time = time.perf_counter() - start

    start = time.perf_counter()
    for query in test:
        tree.nearest(query)
    tree_time = time.perf_counter() - start

    start = time.perf_counter()
    for query in test:
        brute_force_nearest(train, query)
    brute_time = time.perf_counter() - start

    return build_time, tree_time, brute_time


def main() -> None:
    """Runs experiments over several dimensions and dataset sizes."""

    random.seed(0)

    print("| k | numPoints | Build (s) | KD query (s) | Brute force (s) | Speedup |")
    print("|---|---|---|---|---|---|")

    for k in [1, 2, 3, 5, 10, 20]:
        for num_points in [10, 100, 1000, 10000]:
            build_time, tree_time, brute_time = run_experiment(k, num_points)
            speedup = brute_time / tree_time
            print(f"| {k} | {num_points} | {build_time:.4f} | {tree_time:.4f} "
                  f"| {brute_time:.4f} | {speedup:.1f}x |")


if __name__ == "__main__":
    main()
