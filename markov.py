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


def make_sentence(chains, seed_link=None):
    """Takes dictionary of Markov chains; returns a random sentence."""

    ending_punctuation = '.?!'

    sentence = ''

    if seed_link is None:
        # Start only on a capital letter
        current_link = choice(chains.keys())
        while (current_link[0][0] != current_link[0][0].upper()
               or current_link[0][0] in string.punctuation):
            current_link = choice(chains.keys())
    else:
        current_link = seed_link

    n = len(current_link)  # the length of our n-gram
    sentence += ' '.join(current_link)

    while True:
        next_word = choice(chains[current_link])
        pending_link = []

        # Populate the next link in our chain
        # We only want n - 1 words in our pending link because the last place
        # will be occupied by the next word
        i = 0
        while len(pending_link) < (n - 1):
            pending_link.append(current_link[1 + i])
            i += 1

        if next_word is None:
            break  # End of corpus
        elif next_word[-1] in ending_punctuation:
            sentence += ' ' + next_word
            break  # The sentence has ended
        else:
            current_link = make_next_link(pending_link, next_word)
            sentence += ' ' + next_word

    return sentence


def make_next_sentence(sentence, chains):
    """Returns a sentence based on the last n-gram of the previous sentence."""

    n = len(chains.keys()[0])
    words = sentence.split()

    # Check to see if it's even possible to make a next sentence
    if tuple(words[(-1 * n):]) in chains:
        seed_link = tuple(words[(-1 * n):])
        return make_sentence(chains, seed_link)
        # TO DO:
        # Currently prints the seed_link as well as the new sentence
    else:
        return None


def make_next_link(link, word):
    """Returns the next link as a tuple.

    Takes a Markov chain link as a list and the next word to add as a string.
    """

    link.append(word)
    return tuple(link)


def is_under_140(text):
    """Returns true if text is less than 140 characters.

    Used to check for valid tweet length.
    """

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
        test_tweet = tweet + make_sentence(chains) + ' '

        if is_under_140(test_tweet.rstrip()):  # Do not count last space
            tweet = test_tweet
        else:
            return tweet.rstrip()  # Do not include trailing space


# Produce random text
# tweet = make_tweet()

# print tweet
# print len(tweet)

input_path = sys.argv[1]
# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)
# Get a Markov chain
chains = make_chains(input_text, 2)
print make_next_sentence('Would you could you with a fox?', chains)
