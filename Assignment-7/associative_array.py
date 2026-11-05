"""Abstract data type composed of key-value pairs implemented using a hash table"""

from typing import Any
from hash_table import HashTable


class AssociativeArray:
    """Dictionary-like collection of unique keys mapped to values, backed by a hash table."""

    def __init__(self, initial_length: int = 11) -> None:
        """
        Create an empty associative array.

        Args:
            initial_length (int): Initial number of buckets in the underlying hash table.
        """
        self._table = HashTable(initial_length)

    def __setitem__(self, k: Any, v: Any) -> None:
        """
        Insert a key-value pair, or overwrite the value if the key already exists.

        Args:
            k (Any): Key of item.
            v (Any): Value of item.
        """
        self._table.insert(k, v)

    def __getitem__(self, k: Any) -> Any | None:
        """
        Retrieve the value stored at a key.

        Args:
            k (Any): Key to look up.

        Returns:
            Any | None: Value associated with the key, or None if the key does not exist.
        """
        try:
            return self._table.get(k)
        except KeyError:
            return None

    def __contains__(self, k: Any) -> bool:
        """
        Check whether a key exists in the associative array.

        Args:
            k (Any): Key to look up.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        try:
            self._table.get(k)
            return True
        except KeyError:
            return False

    def remove(self, k: Any) -> bool:
        """
        Remove a key-value pair.

        Args:
            k (Any): Key to remove.

        Returns:
            bool: True if the key was removed, False if it did not exist.
        """
        try:
            self._table.remove(k)
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        """
        Return the number of key-value pairs stored.

        Returns:
            int: Number of key-value pairs.
        """
        return self._table.active

    def key_value_pairs(self) -> list[tuple[Any, Any]]:
        """
        Return every key-value pair stored, in no particular order.

        Returns:
            list[tuple[Any, Any]]: List of (key, value) tuples.
        """
        return self._table.items()
