"""Simple Markov chain text generator built on the AssociativeArray."""

import random
from associative_array import AssociativeArray


def build_chain(text: str) -> AssociativeArray:
    """
    Build a Markov chain mapping each word to the list of words that follow it.

    Args:
        text (str): Training text.

    Returns:
        AssociativeArray: Maps each word to a list of possible next words.
    """
    chain = AssociativeArray()
    words = text.split()
    for current, following in zip(words, words[1:]):
        if current in chain:
            chain[current].append(following)
        else:
            chain[current] = [following]
    return chain


def generate(chain: AssociativeArray, start: str, length: int = 50) -> str:
    """
    Generate text by randomly walking the Markov chain.

    Args:
        chain (AssociativeArray): Chain produced by build_chain.
        start (str): Word to start from.
        length (int): Maximum number of words to generate.

    Returns:
        str: Generated text.
    """
    word = start
    output = [word]
    for _ in range(length - 1):
        if word not in chain:
            break
        word = random.choice(chain[word])
        output.append(word)
    return " ".join(output)


if __name__ == "__main__":
    with open("lyrics.txt", encoding="utf-8") as f:
        chain = build_chain(f.read())
    start = random.choice(chain.key_value_pairs())[0]
    print(generate(chain, start))
