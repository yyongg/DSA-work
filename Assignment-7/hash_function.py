"""Hash function implementation"""

from typing import Any

def hash_function(k: Any, l: int) -> int:
    """
    Generate index for hash table using modular hashing and Horner's method
    for generating hash codes.
    
    Args:
        k (Any): key value that we need to create an index for
        l (int): length of the array of values

    Returns:
        int: the converted input key into an index for the array
    """
    prime_base: int = 31
    hash_code: int = 0

    k = str(k)
    for c in k:
        hash_code = hash_code * prime_base + ord(c)

    return hash_code % l
