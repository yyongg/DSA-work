"""Hash function implementation using"""

from typing import Any

def hash_function(k: Any, l: int) -> int:
    """
    Generate index for hash table using modular hashing.
    
    Args:
        k (Any): key value that we need to create an index for
        l (int): length of the array of values

    Returns:
        int: the converted input key into an index for the array
    """
    prime_base: int = 31
    hash_code: int = 0

    k = str(k)
    l_k: int = len(k)
    for i, c in enumerate(k):
        hash_code += ord(c) * prime_base^(l_k-(i+1))

    return hash_code % l
