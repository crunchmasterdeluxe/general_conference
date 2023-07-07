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
    occasions = []
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
        occasions.append("General Conference")

    df = pd.DataFrame(list(zip(titles, authors, dates, contents, occasions)),
                      columns=["title", "author", "date", "text", "occasion"])

    return df


def scrape_bible_dictionary():
    """
    Scrapes bible dictionary to get all main words in Christian vocabulary.

    Returns
    -----
    bible_dict_words (list) : list of words in bible dictionary
    """
    topic_list = requests.get(
        url="https://www.churchofjesuschrist.org/study/scriptures/bd?lang=eng")
    topics = BeautifulSoup(topic_list.text, 'html.parser')

    bible_dict_words = []
    for topic in topics.find_all('a'):
        # retrieve words and remove comma if any
        first_word = (topic.text).split(" ", 1)[0]
        first_word_no_punc = first_word.split(",", 1)[0]
        # append word to bible dict list
        bible_dict_words.append(str(first_word_no_punc).lower())

    return bible_dict_words


def scrape_journal_of_discourses():
    """
    Scrapes all sermons from the Journal of Discourses

    Returns
    -----
    jofd (pandas dataframe) : dataframe with cols "title", "author", "date", "text"
    """
    # Define the base url for the journal of discourses
    base_url = "https://josephsmithfoundation.org/journalofdiscourses/"

    # Create an empty list to store the links to each volume
    volume_links = []

    # Loop through the volume numbers from 1 to 26
    for i in range(1, 27):
        # Append the volume number to the base url and add it to the list
        volume_link = base_url + "topics/volumes/volume-" + \
            str(i) + "/?print=print-search"
        volume_links.append(volume_link)

    titles = []
    volume_text = []
    authors = []
    dates = []
    occasions = []

    # Loop through each volume link
    for volume_link in volume_links:

        # Get the html content of the discourse page
        discourse_page = requests.get(volume_link)
        discourse_page
        # Parse the html content using BeautifulSoup
        discourse_soup = BeautifulSoup(discourse_page.content, "html.parser")

        for (title, text) in zip(discourse_soup.find_all("h1", class_="entry-title"), discourse_soup.find_all("div", class_="entry-content")):

            text = str(text).strip().replace(',', '')
            text = re.sub('\n', '', text)
            text = re.sub('</div>', '\n', text)

            heading = re.search(r'<em>(.*?)</em>', text).group(1)

            # Pull out the author
            try:
                author = re.search(r'by (.*?) Delivered', heading)
                if author != None:
                    author = author.group(1)
            except:
                author = re.search(r'by (.*?) delivered', heading)
                if author != None:
                    author = author.group(1)
            finally:
                if author == None:
                    author = ""

            # Pull out the month
            month_number = None
            month = re.findall(r'(?:(Jan)(?:uary)?)', heading)
            if month != []:
                month_number = "01"
            month = re.findall(r'(?:(Feb)(?:ruary)?)', heading)
            if month != []:
                month_number = "02"
            month = re.findall(r'(?:(Mar)(?:ch)?)', heading)
            if month != []:
                month_number = "03"
            month = re.findall(r'(?:(Apr)(?:il)?)', heading)
            if month != []:
                month_number = "04"
            month = re.findall(r'(?:(May))', heading)
            if month != []:
                month_number = "05"
            month = re.findall(r'(?:(Jun)(?:e)?)', heading)
            if month != []:
                month_number = "06"
            month = re.findall(r'(?:(Jul)(?:y)?)', heading)
            if month != []:
                month_number = "07"
            month = re.findall(r'(?:(Aug)(?:ust)?)', heading)
            if month != []:
                month_number = "08"
            month = re.findall(r'(?:(Sep)(?:tember)?)', heading)
            if month != []:
                month_number = "09"
            month = re.findall(r'(?:(Oct)(?:ober)?)', heading)
            if month != []:
                month_number = "10"
            month = re.findall(r'(?:(Nov)(?:ember)?)', heading)
            if month != []:
                month_number = "11"
            month = re.findall(r'(?:(Dec)(?:ember)?)', heading)
            if month != []:
                month_number = "12"

            # Pull out the day
            try:
                day = re.findall(r'\d{2} ', heading)
                if day != []:
                    day = day[-1]
                else:
                    single_digit_day = re.findall(r'\d{1} ', heading)[-1]
                    day = "0{}".format(single_digit_day)
            except:
                day = "01"

            # Pull out the year
            try:
                year = str(re.findall(r'\d{4}', heading)[-1])
            except:
                year = None

            if year != None and month_number != None:
                date = "{}-{}-{}".format(year, month_number, day)
            else:
                date = None

            text = re.sub('<em>.*?</em>', '', text)
            text = re.sub('<.*?>', '', text)

            title = str(title).strip().replace(',', '')
            title = re.sub('.*?"entry-title">', '', title)
            title = re.sub('</h1>', '', title)

            titles.append(title)
            volume_text.append(text)
            authors.append(author)
            dates.append(date)
            occasions.append("Journal of Discourses")

    jofd = pd.DataFrame(list(zip(titles, authors, dates, volume_text, occasions)),
                        columns=["title", "author", "date", "text", "occasion"])

    return jofd
