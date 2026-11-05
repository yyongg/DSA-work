"""Find the next prime number."""

import math

def is_prime(num: int) -> bool:
    """Returns True if num is prime, otherwise False."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    # Skip even numbers and multiples of 3
    if num % 2 == 0 or num % 3 == 0:
        return False

    # Check factors up to the square root, skipping even numbers
    for i in range(5, int(math.sqrt(num)) + 1, 6):
        if num % i == 0 or num % (i + 2) == 0:
            return False
    return True

def next_prime(n: int) -> int:
    """Returns the smallest prime number strictly greater than n."""
    if n < 2:
        return 2

    prime = n
    found = False

    # Continuously increment and test until a prime is found
    while not found:
        prime += 1
        if is_prime(prime):
            found = True

    return prime
