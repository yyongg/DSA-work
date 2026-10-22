"""Smith-Waterman local sequence alignment using dynamic programming."""

import re
import sys

MATCH = 3
MISMATCH = -3
GAP = -2


def match_score(x: str, y: str) -> int:
    """
    Score for lining up two characters.
    return MATCH if they are equal, MISMATCH otherwise
    """
    if x == y:
        return MATCH
    return MISMATCH


def score_matrix(a: str, b: str) -> list[list[int]]:
    """
    Fill the dynamic programming table. H[i][j] is the best score of a
    local alignment ending at a[i-1] and b[j-1], never going below 0.
    param a the first sequence (rows)
    param b the second sequence (columns)
    return the (len(a) + 1) x (len(b) + 1) score table
    """
    n = len(a)
    m = len(b)
    H = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diagonal = H[i - 1][j - 1] + match_score(a[i - 1], b[j - 1])
            up = H[i - 1][j] + GAP
            left = H[i][j - 1] + GAP
            H[i][j] = max(0, diagonal, up, left)

    return H


def smith_waterman(a: str, b: str) -> tuple[int, str, str]:
    """
    Find the best local alignment of a and b. Start at the highest cell
    in the table and trace back until a 0 is reached.
    param a the first sequence
    param b the second sequence
    return (score, aligned a, aligned b), with '-' marking gaps
    """
    H = score_matrix(a, b)

    # find the cell with the highest score
    best_score = 0
    best_i = 0
    best_j = 0
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if H[i][j] > best_score:
                best_score = H[i][j]
                best_i = i
                best_j = j

    # trace back from the best cell until the score drops to 0
    aligned_a: list[str] = []
    aligned_b: list[str] = []
    i = best_i
    j = best_j
    while H[i][j] > 0:
        if H[i][j] == H[i - 1][j - 1] + match_score(a[i - 1], b[j - 1]):
            aligned_a.append(a[i - 1])
            aligned_b.append(b[j - 1])
            i -= 1
            j -= 1
        elif H[i][j] == H[i - 1][j] + GAP:
            aligned_a.append(a[i - 1])
            aligned_b.append("-")
            i -= 1
        else:
            aligned_a.append("-")
            aligned_b.append(b[j - 1])
            j -= 1

    # the traceback built the strings backwards
    aligned_a.reverse()
    aligned_b.reverse()
    return best_score, "".join(aligned_a), "".join(aligned_b)


def show_alignment(aligned_a: str, aligned_b: str, width: int = 60) -> str:
    """
    Print the two aligned strings in rows, with '|' under matching letters.
    param aligned_a, aligned_b the aligned sequences
    param width the number of characters per row
    return the alignment as text
    """
    bars = ""
    for k in range(len(aligned_a)):
        if aligned_a[k] == aligned_b[k]:
            bars += "|"
        else:
            bars += " "

    rows: list[str] = []
    for start in range(0, len(bars), width):
        end = start + width
        rows.append(aligned_a[start:end] + "\n" + bars[start:end] + "\n" + aligned_b[start:end] + "\n")
    return "\n".join(rows)


def read_kotlin(path: str) -> dict[str, str]:
    """
    Read every `val name = "..."` string out of a Kotlin file.
    param path the Kotlin file
    return a dict from variable name to sequence
    """
    with open(path, encoding="utf-8") as f:
        return dict(re.findall(r'val\s+(\w+)\s*=\s*"([^"]*)"', f.read()))


if __name__ == "__main__":
    seqs = read_kotlin(sys.argv[1])
    target = seqs["targetGenome"]
    query = seqs["testAgainst"]

    score, aligned_query, aligned_target = smith_waterman(query, target)
    print(f"Score: {score}\n")
    print(show_alignment(aligned_query, aligned_target))
    print("Best matching sequence in targetGenome:")
    print(aligned_target.replace("-", ""))
