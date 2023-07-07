from interesting_words import bible_dictionary_words
from f_manipulation import make_word_cloud, create_word_count, count_words_of_interest
from f_scraping import build_conference_links, get_talk_links, get_talk_content

import pandas as pd
import sqlite3


def create_charts():
    """
    Queries all talks from db and creates wordclouds
    and compares word counts
    """
    conn = sqlite3.connect('church_content.db')

    query = """
    SELECT * FROM talks;
    """
    df = pd.read_sql(query, conn)

    # could narrow df down to a few conferences if desired
    # df = df.loc[(df['date'] == '2023-04-01') | (df['date'] == '2022-10-01')]

    specific_text = ""
    for i in df['text']:
        specific_text += i

    # Create word cloud
    make_word_cloud(text=specific_text,
                    destination="./wordcloud.png")
    # Get count of ocurrences of each word
    total_counts = create_word_count(specific_text)
    # Count words of interest
    interesting_word_counts = count_words_of_interest(word_count_dict=total_counts,
                                                      interesting_words=bible_dictionary_words)
    print(interesting_word_counts)

    return


if __name__ == '__main__':
    create_charts()
