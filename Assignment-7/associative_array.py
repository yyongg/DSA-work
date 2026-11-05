"""Abstract data type composed of key-value pairs implemented using a hash table"""

from typing import Any
from hash_table import HashTable


class AssociativeArray:
    def __init__(self, initial_length: int = 11) -> None:
        self._table = HashTable(initial_length)

    def __setitem__(self, k: Any, v: Any) -> None:
        self._table.insert(k, v)

    def __getitem__(self, k: Any) -> Any | None:
        try:
            return self._table.get(k)
        except KeyError:
            return None

    def __contains__(self, k: Any) -> bool:
        try:
            self._table.get(k)
            return True
        except KeyError:
            return False

    def remove(self, k: Any) -> bool:
        try:
            self._table.remove(k)
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        return self._table.active

    def key_value_pairs(self) -> list[tuple[Any, Any]]:
        return self._table.items()
