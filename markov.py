from random import choice
import sys


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    return open(file_path).read()


def make_chains(text_string, n=2):
    """Takes input text as string; returns _dictionary_ of markov chains.

    Also takes an integer, n, to specify length of n-gram.

    A chain will be a key that consists of a tuple that is an n-gram
    (word1, word2,...,wordn) and the value would be a list of the word(s)
    that follow those n-words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    for i in range(len(words) - (n - 1)):
        ngram = []

        for incr in range(0, n):
            ngram.append(words[i + incr])

        # Find word that follows sec_word
        try:
            next_word = words[i + n]
        except IndexError:
            next_word = None

        ngram = tuple(ngram)
        chains[ngram] = chains.get(ngram, [])
        chains[ngram].append(next_word)

    return chains


def make_text(chains, n=2):
    """Takes dictionary of markov chains; returns random text."""

    text = ""
    current_link = choice(chains.keys())
    text += ' '.join(current_link)

    while True:
        next_word = choice(chains[current_link])
        next_link = []

        for incr in range(0, n - 1):
            next_link.append(current_link[1 + incr])

        next_link.append(next_word)

        if next_word is None:
            break
        else:
            current_link = tuple(next_link)
            text += ' ' + next_word

    return text


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, 3)

# Produce random text
random_text = make_text(chains, 3)

print random_text
