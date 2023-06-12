from bs4 import BeautifulSoup
import requests
import datetime
import re
import pandas as pd


def list_conference_links():
    """
    Gets the list of conferences

    Returns
    -----
    - conf_links (list) : urls of all conferences
    """
    # get conference link structure
    all_talks = requests.get(
        url="https://www.churchofjesuschrist.org/study/general-conference?lang=eng")
    all_talk_html = BeautifulSoup(all_talks.text, 'html.parser')
    conf_links = []
    for link in all_talk_html.find_all('a'):
        conf_links.append(link.get('href'))
    return conf_links


def build_conference_links(starting_year):
    """
    Builds a list of all conference urls which can be drilled into
    to get a list of talks from each conference

    Args
    -----
    - starting_year (int) : earliest year for which you'd like conferences

    Returns
    -----
    - conf_links (list) : list of tuples including
        - conference links within desired time period
        - estimated date of conference
    """
    year = starting_year
    # make sure we're in at least May of current year
    ending_year = (datetime.datetime.now() -
                   datetime.timedelta(days=140)).strftime("%Y")
    ending_month = datetime.datetime.now().strftime("%m")

    # build conference links
    conf_links = []
    while year <= int(ending_year):
        conf_links.append(('https://www.churchofjesuschrist.org/study/general-conference/{}/{}?lang=eng'.format(
            str(year), "04"), "{}-{}".format(str(year), "04-01")))
        if int(ending_month) <= 10 and year == int(ending_year):
            pass
        else:
            conf_links.append(('https://www.churchofjesuschrist.org/study/general-conference/{}/{}?lang=eng'.format(
                str(year), "10"), "{}-{}".format(str(year), "10-01")))
        year += 1

    return conf_links


def get_talk_links(conf_links):
    """
    Gets the urls for each talk in each conerence passed to it.
    The function also cleans out links that are not talks.

    Args
    -----
    - conf_links (list) : list of tuples of urls of conferences and dates

    Returns
    -----
    - link_list (list) : list of tuples including:
        - url of a conference talk
        - estimated date talk was given
    """
    link_list = []
    for conf_url in conf_links:
        conf_talks = requests.get(url=conf_url[0])
        conf_talks_html = BeautifulSoup(conf_talks.text, 'html.parser')
        for link in conf_talks_html.find_all('a'):
            # clean out undesired urls
            link_url = link.get('href')
            iso_date_match = re.search(r'(general-conference/\d+\?)', link_url)
            human_date_match = re.search(
                r'(general-conference/\d+/\d+\?)', link_url)
            saturday_session_match = re.search(
                r'(/\d+/\d+/saturday)', link_url)
            sunday_session_match = re.search(r'(/\d+/\d+/sunday)', link_url)
            # append remaining urls to list
            if iso_date_match == None and human_date_match == None and saturday_session_match == None and sunday_session_match == None:
                link_list.append(
                    ("https://www.churchofjesuschrist.org{}".format(link_url), conf_url[1]))
    return link_list


def get_talk_content(talk_links):
    """
    Gets the title, author, date, and content of each talk

    NOTE: Some html id tags don't return a value, 
    hence all the try-excepts.

    Args
    -----
    - talk_links (list) : list of tuples of all talks and their dates

    Returns
    -----
    - df (dataframe) : dataframe including title, author, est. date,
      and content of each talk
    """
    titles = []
    authors = []
    dates = []
    contents = []
    for talk_url in talk_links:
        talk = requests.get(url=talk_url[0])
        talk_html = BeautifulSoup(talk.text, 'html.parser')
        # get title, author, and talk body
        try:
            titles.append(talk_html.find(id="title1").string)
        except:
            titles.append("")
        try:
            author = talk_html.find(id="p1").string
            if author == None:
                author = talk_html.find(id="p1").get_text()
            if author[:3] == "By ":
                authors.append(author[3:])
            if author[:5] == "  By ":
                authors.append(author[5:])
            elif author[:13] == "Presented by ":
                authors.append(author[13:])
            else:
                authors.append(author)
        except:
            authors.append("")
        dates.append(talk_url[1])
        try:
            contents.append(talk_html.find(
                "div", {"class": "body-block"}).get_text())
        except:
            contents.append("")

    df = pd.DataFrame(list(zip(titles, authors, dates, contents)),
                      columns=["title", "author", "date", "text"])

    return df
