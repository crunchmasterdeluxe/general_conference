from f_manipulation import make_word_cloud, create_word_count, count_words_of_interest
from f_scraping import build_conference_links, get_talk_links, get_talk_content

import pandas as pd
import sqlite3
import time


def get_talks():
    """
    Scrapes general conferences talks and puts content into sqlite db.

    NOTE: Earliest available conference on church website is 1971.
    """
    print("Retrieving talks...")
    start = time.perf_counter()
    year = 1971

    conf_links = build_conference_links(starting_year=year)
    talk_links = get_talk_links(conf_links)
    df = get_talk_content(talk_links)

    conn = sqlite3.connect("church_content.db")

    df.to_sql('talks', conn, if_exists='append')

    print("\n====================")
    print("Completed in", time.perf_counter() - start, "s")

    return


if __name__ == '__main__':
    get_talks()
