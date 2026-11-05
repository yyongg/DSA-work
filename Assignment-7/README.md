# Assignment 7 – Associative Array

## Markov Text Generator

[markov.py](markov.py) builds a first-order (one-word) Markov chain on top of `AssociativeArray`.
Each word is a key, and its value is the list of words that come right after it in the training text.
To generate text, it starts from a word and keeps picking a random follower.

### Training data

`lyrics.txt` is a collection of lyrics from Taylor Swift songs. The data is from: https://github.com/shaynak/taylor-swift-lyrics/tree/main

| Statistic | Value |
|---|---|
| Total words | 82,120 |
| Unique words (keys in the associative array) | 8,435 |
| Most followers for one word | 3,246 |

### Example

Trained on the toy sentence
`the cat sat on the mat and the dog sat on the cat and the mat sat still`,
starting from `the`, with 12 words:

```
the cat and the dog sat on the cat and the mat
the mat and the mat sat still
the cat sat on the mat sat on the mat and the
```

Each pair of neighbouring words appears somewhere in the training text, but the full sequence is new.
Generation stops early when it reaches a word with no followers (`still`).

### Results on the lyrics

Run `python markov.py` to generate 50 words from the lyrics corpus.
The output reads as locally fluent but globally incoherent.
Because each choice depends on only one previous word, the chain often runs through
repeated chorus lines and copies short phrases of the source word for word.
A higher-order chain (keyed on the previous 2–3 words) would sound more fluent but copy even more.
