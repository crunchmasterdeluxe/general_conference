# General Conference Insights
The objective of this script is twofold:
1. Scrape conference talks within desired time frame.
2. Play with the results to discover trends and insights.

## Running
Clone the repo into a local dir. Navigate to the directory and run the command `python3 main.py`

## Step 1: Scrape
[This url](https://www.churchofjesuschrist.org/study/general-conference?lang=eng) contains the tree of conferences from which the talks will be scraped. 

You can use the `list_conference_links()` function to see all conference urls.

`main.py` then drills down form conferences into the talk list into the talk content and puts the results into a dataframe.

## Step 2: Manipulate
Questions of interest are:
- See which words are used most often in general conference (word cloud).
- List all words and their number of ocurrences.
- See the number of ocurrences for words/people of interest.
- See how different are topics today vs topics in the journal of discourses.
- See if certain people focus on certain topics more.
- See if a certain person's talks change from the time they begin their calling to present day.

More questions to come!

## Results
Results are placed into a dataframe and into a csv in this repo for convenience/visibility.

Here are modern word usages (first image) compared to 1850s word usages (second image)

###Modern Word Cloud
![conference](https://github.com/crunchmasterdeluxe/general_conference/assets/83776204/a3eee3fc-dacd-400c-aacd-231fe670c1c9)

###Journal of Discourses Word Cloud
<img width="934" alt="Screenshot 2023-06-12 at 9 20 42 PM" src="https://github.com/crunchmasterdeluxe/general_conference/assets/83776204/80616b5a-4040-4459-895a-4f233f49d7c2">


Here are word counts between the two eras. Keep in mind that there are much more words collected from general conference than from the journal of discourses. This will need to be changed to reflect word percentage of usage rather than counts.
![text_comparison_1](https://github.com/crunchmasterdeluxe/general_conference/assets/83776204/9335fe3a-e18b-472d-b233-e2e28f589896)



## Personal Note

One note as I dig into the data is that "God"/"Lord"/"Jesus Christ" are by far the most talked about word/phrase in general conference.

It is nice to see that He is the center of discussion, even as the culture and focus over the decades has shifted.
