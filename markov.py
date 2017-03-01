from random import choice
import sys
import string


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

    # Remember n is the length of our n-gram!!
    chains = {}

    words = text_string.split()

    # Populate our n-gram
    for i in range(len(words) - (n - 1)):
        ngram = []

        for incr in range(0, n):
            ngram.append(words[i + incr])

        # Find the word that follows the last member of our ngram
        try:
            next_word = words[i + n]
        except IndexError:
            next_word = None

        ngram = tuple(ngram)
        chains[ngram] = chains.get(ngram, [])
        chains[ngram].append(next_word)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns a random sentence."""

    # Maybe add a way for users to specify amount of sentences they want

    ending_punctuation = '.?!'

    text = ""
    # Start only on a capital letter
    current_link = choice([key for key in chains.keys() if key[0][0] == key[0][0].upper()
                                                           and key[0][0] not in string.punctuation])
    n = len(current_link) # the length of our n-gram
    text += ' '.join(current_link)

    while True:
        next_word = choice(chains[current_link])
        next_link = []

        # Populate the next link in our chain
        for incr in range(0, n - 1):
            next_link.append(current_link[1 + incr])

        if next_word is None:
            break # There are no more words left
        elif next_word[-1] in ending_punctuation:
            current_link = make_next_link(next_link, next_word)
            text += ' ' + next_word
            break # The sentence has ended
        else:
            current_link = make_next_link(next_link, next_word)
            text += ' ' + next_word

    return text


def make_next_link(link, word):
    """Returns the next link as a tuple."""

    link.append(word)
    return tuple(link)


def is_under_140(text):
    """Returns true if text is less than or equal to 140 characters."""

    return len(text) < 140


def make_tweet():
    """Returns a Markov tweet."""

    input_path = sys.argv[1]
    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)
    # Get a Markov chain
    chains = make_chains(input_text, 3)
    tweet = ''

    while True:
        test_tweet = tweet + make_text(chains) + ' '
        if is_under_140(test_tweet):
            tweet = test_tweet
        else:
            return tweet


# Produce random text
tweet = make_tweet()

print tweet
print len(tweet)
