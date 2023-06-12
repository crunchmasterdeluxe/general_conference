# General Conference
The objective of this script is twofold:
1. Scrape conference talks within desired time frame.
2. Play with the results to discover trends and insights.

## Running
Clone the repo into a local dir. Navigate to the directory and run the command `python3 main.py`

## Step 1: Scrape
This url(https://www.churchofjesuschrist.org/study/general-conference?lang=eng) contains the tree of conferences from which the talks will be scraped. 

You can use the `list_conference_links()` function to see all conference urls.

`main.py` then drills down form conferences into the talk list into the talk content and puts the results into a dataframe.

## Step 2: Manipulate
Questions of interest are:
1. See which words are used most often in general conference (word cloud).
2. List all words and their number of ocurrences.
3. See the number of ocurrences for words/people of interest.

More questions to come!

## Results
Results are placed into a dataframe and into a csv in this repo for convenience/visibility.

## Personal Note
One note as I dig into the data is that "Jesus Christ" is by far the most talked about word/phrase in general conference.

It is nice to see that He is the center of discussion, even as the culture and focus over the decades has shifted.
