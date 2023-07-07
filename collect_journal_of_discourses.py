from f_manipulation import make_word_cloud, create_word_count, count_words_of_interest
from f_scraping import build_conference_links, get_talk_links, get_talk_content, scrape_journal_of_discourses

import pandas as pd
import sqlite3
import time


def get_talks():
    """
    Scrapes general conferences talks and puts content into sqlite db.

    """
    print("Retrieving talks...")
    start = time.perf_counter()

    jofd = scrape_journal_of_discourses()

    conn = sqlite3.connect("church_content.db")

    jofd.to_sql('talks', conn, if_exists='append')

    print("\n====================")
    print("Completed in", time.perf_counter() - start, "s")

    return


if __name__ == '__main__':
    get_talks()
