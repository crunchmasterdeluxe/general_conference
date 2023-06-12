from interesting_words import people, principles
from manipulation import make_word_cloud, create_word_count, count_words_of_interest
from scraping import build_conference_links, get_talk_links, get_talk_content

import pandas as pd


def main():
    """
    Scrapes general conferences talks and puts content into csv.
    Calls manipulation functions to answer questions about text

    """
    # path to folder where final csv will be stored
    local_doc_path = "/Users/andy/Desktop/Python/Hobby/general_conference/"
    year = 2010

    conf_links = build_conference_links(starting_year=year)
    talk_links = get_talk_links(conf_links)
    df = get_talk_content(talk_links)

    # save to local file
    df.to_csv("{}talks_{}-present.csv".format(local_doc_path, year))

    # could narrow df down to a few conferences if desired
    # df = df.loc[(df['date'] == '2023-04-01') | (df['date'] == '2022-10-01')]
    specific_text = ""
    for i in df['text']:
        specific_text += i

    # Create word cloud
    make_word_cloud(text=specific_text,
                    destination="{}wordcloud.png".format(local_doc_path))
    # Get count of ocurrences of each word
    total_counts = create_word_count(specific_text)
    # Count words of interest
    interesting_word_counts = count_words_of_interest(word_count_dict=total_counts,
                                                      interesting_words=people)
    print(interesting_word_counts)

    return


if __name__ == '__main__':
    main()
