from random import choice


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    return open(file_path).read()


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split() 

    for i in range(len(words) - 1):
        first_word = words[i]

        # Wrap around back to the beginning of the list if the
        # index does not exist
        sec_word = words[(i + 1) % len(words)]

        # Find word that follows sec_word
        next_word = words[(i + 2) % len(words)]

        bigram = (first_word, sec_word)
        chains[bigram] = chains.get(bigram, [])
        chains[bigram].append(next_word)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    text = ""
    current_link = choice(chains.keys())
    text += current_link[0] + ' ' + current_link[1]

    while current_link in chains:
        next_word = choice(chains[current_link])
        current_link = (current_link[1], next_word)

        if current_link in chains:
            text += ' ' + next_word

    return text


input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print random_text
