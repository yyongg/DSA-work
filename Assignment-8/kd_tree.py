"""K-D tree and brute force nearest neighbor implementation."""

import math
from typing import Sequence

Point = tuple[float, ...]


def squared_distance(a: Point, b: Point) -> float:
    """Computes the squared Euclidean distance between two points.

    The square root is skipped because it does not change which point is closer.

    Args:
        a: The first point.
        b: The second point, with the same dimension as a.

    Returns:
        The sum of squared differences of each coordinate.
    """

    total = 0.0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return total


def brute_force_nearest(points: Sequence[Point], query: Point) -> Point:
    """Finds the nearest neighbor by checking the distance to every point.

    Args:
        points: The k-dimensional points to search.
        query: The k-dimensional point to find the nearest neighbor of.

    Returns:
        The point in points closest to query.
    """

    best_point = points[0]
    best_dist = squared_distance(best_point, query)

    for point in points:
        dist = squared_distance(point, query)
        if dist < best_dist:
            best_point = point
            best_dist = dist

    return best_point


class KDNode():
    """A single node in the K-D tree.

    Attributes:
        point: The point stored at this node.
        axis: The dimension this node splits on.
        left: Subtree of points with a smaller value on axis.
        right: Subtree of points with a greater or equal value on axis.
    """

    def __init__(self, point: Point, axis: int) -> None:
        self.point = point
        self.axis = axis
        self.left: KDNode | None = None
        self.right: KDNode | None = None


class KDTree():
    """K-D tree built from a list of k-dimensional points.

    Attributes:
        k: The dimension of the points.
        root: The root node of the tree.
        best_point: The closest point found so far during a search.
        best_dist: The squared distance to best_point.
    """

    def __init__(self, points: Sequence[Point]) -> None:
        """Builds a balanced K-D tree from points.

        Args:
            points: The k-dimensional points to store in the tree.
        """

        self.k = len(points[0])
        self.root = self._build(list(points), 0)
        self.best_point = points[0]
        self.best_dist = math.inf

    def _build(self, points: list[Point], depth: int) -> KDNode | None:
        """Recursively builds a subtree by splitting on the median point.

        Args:
            points: The points to put in this subtree.
            depth: The depth of this subtree, used to pick the split axis.

        Returns:
            The root of the subtree, or None if points is empty.
        """

        if len(points) == 0:
            return None

        axis = depth % self.k

        def get_axis_value(point: Point) -> float:
            return point[axis]

        points = sorted(points, key=get_axis_value)
        mid = len(points) // 2

        node = KDNode(points[mid], axis)
        node.left = self._build(points[:mid], depth + 1)
        node.right = self._build(points[mid + 1:], depth + 1)
        return node

    def nearest(self, query: Point) -> Point:
        """Finds the nearest neighbor of query using the tree.

        Args:
            query: The k-dimensional point to find the nearest neighbor of.

        Returns:
            The point in the tree closest to query.
        """

        self.best_dist = math.inf
        self._nearest(self.root, query)
        return self.best_point

    def _nearest(self, node: KDNode | None, query: Point) -> None:
        """Recursively searches a subtree, skipping branches that cannot be closer.

        Updates self.best_point and self.best_dist when a closer point is found.

        Args:
            node: The root of the subtree to search.
            query: The point to find the nearest neighbor of.
        """

        if node is None:
            return

        dist = squared_distance(node.point, query)
        if dist < self.best_dist:
            self.best_point = node.point
            self.best_dist = dist

        # Distance from the query to this node's splitting plane
        diff = query[node.axis] - node.point[node.axis]

        # Search the side of the plane the query is on first
        if diff < 0:
            near = node.left
            far = node.right
        else:
            near = node.right
            far = node.left

        self._nearest(near, query)

        # The other side can only hold a closer point if the plane is closer than best
        if diff ** 2 < self.best_dist:
            self._nearest(far, query)
