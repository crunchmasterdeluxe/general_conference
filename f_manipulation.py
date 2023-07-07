import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import OrderedDict
import numpy as np


def make_word_cloud(text, destination):
    """
    Generates a word cloud of given text

    Args
    -----
    - text (str) : continuous string of talks

    Returns
    -----
    - plt (obj) : plotly object of wordcloud image
    """
    # remove bad characters so they're not treated as words
    punctuation_characters = ["\n", ".", "?", "!", ",",
                              ";", ":", "â", "\x80\x99s", "\x80\x9d", "\x80\x99t"]
    for char in punctuation_characters:
        all_text = text.replace(char, " ")

    # define plotly obj
    plt.subplots(figsize=(12, 12))
    wordcloud = WordCloud(
        background_color='white',
        width=512,
        height=384
    ).generate(all_text)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig(destination)

    return plt


def create_word_count(text):
    """
    Puts together a list of all words used and their 
    counts in descending order

    Args
    -----
    - text (str) : continuous string of talks
    """
    counts = dict()
    words = text.split()

    # get count
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    # order
    keys = list(counts.keys())
    values = list(counts.values())
    sorted_value_index = np.argsort(values)[::-1]
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}


def count_words_of_interest(word_count_dict, interesting_words):
    """
    Counts ocurrence of words of interest

    Args
    -----
    - word_count_dict (dict) : dict of words and their counts
    - interesting_words (list) : list of words that user would like to see counts of

    Returns
    -----
    - interesting_word_counts (dict) : count of each word in question, desc order
    """
    interesting_word_counts = {}
    for i in word_count_dict.keys():
        if i in interesting_words:
            name = i
            if i == "Smith":
                name = "Joseph Smith"
            if i == "Christ":
                name = "Jesus Christ"
            interesting_word_counts[name] = word_count_dict[i]
    return interesting_word_counts
