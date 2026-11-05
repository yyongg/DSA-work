"""Hash table implementation"""

from typing import Any
from hash_function import hash_function
from next_prime import next_prime

class HashTable():
    """Implementation of hash table using separate chaining and prime number sizes"""

    def __init__(self, initial_length: int) -> None:
        if initial_length < 1:
            raise ValueError("Set initial length greater than 0")

        self.length = initial_length
        self.table: list[list[tuple[Any,Any]]] = [[] for _ in range(self.length)]
        self.active = 0

    def _rehash(self):
        """Helper function to rehash when the table fills up"""

        new_length = next_prime(self.length * 2)
        new_table = HashTable(new_length)
        for bucket in self.table:
            for pair in bucket:
                new_table.insert(pair[0],pair[1])

        self.length = new_length
        self.table = new_table.table

    def _search_bucket(self, bucket: list[tuple[Any,Any]], k: Any) -> int:
        """Search bucket for a key value, returns the index in the bucket"""

        for i, pair in enumerate(bucket):
            if pair[0] == k:
                return i

        raise KeyError("Key does not exist in bucket")

    def get(self, k: Any) -> Any:
        """
        Retrieve value at specified key.
        
        Args:
            k (Any): Key to look up.
        
        Returns:
            Any: Value associated with key in hash table.
        """

        hashed_key = hash_function(k,self.length)
        return self.table[hashed_key][self._search_bucket(self.table[hashed_key],k)][1]

    def insert(self, k: Any, v: Any):
        """
        Inserts/puts a new key-value pair into the hash table.

        Args:
            k (Any): Key of item
            v (Any): Value of item
        """
        # rehash if table is full
        if self.active == self.length:
            self._rehash()

        # apply hash function to key
        hashed_key = hash_function(k, self.length)

        # replace kv pair if key exists in bucket, else append kv pair
        try:
            i = self._search_bucket(self.table[hashed_key], k)
            self.table[hashed_key][i] = (k,v)

        except KeyError:
            # append another kv pair into bucket if key doesn't exists
            self.table[hashed_key].append((k,v))
            self.active += 1

    def remove(self,k: Any):
        """
        Remove key-value pair from hash table.

        Args:
            k (Any): Key to be removed from hash_table
        """

        hashed_key = hash_function(k,self.length)
        del self.table[hashed_key][self._search_bucket(self.table[hashed_key],k)]
        self.active -= 1

    def items(self) -> list[tuple[Any, Any]]:
        """Return every key-value pair stored in the table."""
        return [pair for bucket in self.table for pair in bucket]

    def __getitem__(self, k: Any):
        return self.get(k)
