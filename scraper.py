"""A rough implementation of an Alexa skill using flask-ask, beautiful soup and scikit-learn. The machine learning
   algorithm used for updating the user preferences is called tf-idf (Term Frequency-Inverse Document Frequency). It
   looks through a set of documents and finds the most common words among all the documents and ranks them by their
   frequency scores. Right now the machine learning itself is very slow because it's trawling through a set of docs on
   the local machine. More development is needed to optimize and streamline the process. Each document contains a single
   article scraped directly from the html using beautiful soup which is also very slow. Maybe with an API key, the
   article scraping can be very easily streamlined. Also, while tfidf is a the industry standard, there must be a
   separate machine learning and training algorithm for implementing machine learning using the AP's metadata tagging
   system.
             ___________________________________________________________________________________________________
            |                                                                                                   |
            |This skill was developed for the Management 8054 class as a demonstration for the Associated Press.|
            |___________________________________________________________________________________________________|

   The app can do the following:
   1. Search for a term and return the headlines related to that
   2. Use the text from the top 3 headlines in 5 separate preferences to learn the user's preferences and update
   the in-built preference accordingly. The user can set initial preferences
   3. Play an archival recording of the AP's coverage of the 1985 Challenger disaster

   Developed by:
   Natarajan Mahalingam
   2017 Crosby MBA Spring Entry
   University of Missouri, Columbia
   April, 2017"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask_ask import Ask, question, statement, audio
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import os
from fnmatch import fnmatch

app = Flask(__name__)
ask = Ask(app, '/alexa')

'''Flask ask function for the prompt to the user on launch. Also clears the contents of all the text files'''


@ask.launch
def new_ask():
    clear_everything()
    welcome = render_template('welcome')
    reprompt = render_template('reprompt')
    return question(welcome).reprompt(reprompt)


'''Traverses the directory and finds every single file with the .txt extension.
   This is needed because the logic is such that we are using the TfidfVectorizer class from the sklearn module
   As of right now it needs each document in a separate file i.e., the set of text documents that we are traversing and
   fitting our data with. This is not very efficient and right now I don't fully understand how it works. But for
   demonstration purposes it works well enough. Each document contains one news article scraped from the html'''


def get_document_filenames(document_path=r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp'):
    pattern = "*.txt"

    for path, subdirs, files in os.walk(document_path):
        for name in files:
            if fnmatch(name, pattern):
                return [os.path.join(path, name)]


'''The function that creates the vectorizer object. Add any extra unnecessary words to the list. Needs a lot more
   testing '''


def create_vectorizer():
    # Arguments here are tweaked for working with a particular data set.
    # All that's really needed is the input argument.
    my_additional_stop_words = ['says', 'week', 'year', 'said', 'use']

    return TfidfVectorizer(input='filename', max_features=50, min_df=1,
                           token_pattern='(?u)\\b[a-zA-Z]\\w{2,}\\b',
                           max_df=1000,
                           stop_words=text.ENGLISH_STOP_WORDS.union(my_additional_stop_words),
                           ngram_range=(1, 1))


'''Function that gets the feature names and scores. This calls the update_recommendations function which updates the
   text file for our preferences'''


def display_scores(vectorizer, tfidf_result):
    scores = zip(vectorizer.get_feature_names(),
                 np.asarray(tfidf_result.sum(axis=0)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    y = []
    for item in sorted_scores[:5]:
        y.append(item[0])
    update_recommendations(y)


'''Unnecessary. Remove this'''


def update_tfidf():
    vectorizer = create_vectorizer()
    tfidf_result = vectorizer.fit_transform(get_document_filenames())
    display_scores(vectorizer, tfidf_result)


'''Simply adds 2 words in the search term with the +. Mainly because the search url requires it'''


def parse_word(word):
    word_list = word.split(' ')
    reshaped_word = '+'.join(word_list)
    all_heads = scrape_simple(reshaped_word)
    return all_heads


'''Function used for a single search term intent. Scrapes the searched page and returns the headlines for the
   searched term'''


def scrape_simple(word):
    full_list = []
    ap = 'http://hosted.ap.org/dynamic/external/search.hosted.ap.org/wireCoreTool/Search?SITE=AP&SECTION=HOME' \
         '&TEMPLATE=DEFAULT&query='

    page = urlopen(ap + word)  # Add the url and word to search and open using urllib's urlopen function

    soup = BeautifulSoup(page, 'lxml')  # 'Soupify' the page using beautiful soup. easier to search for using BS again

    all_heads = soup.find_all('span', {'class': 'latestnews'})  # The AP uses a span tag with class latestnews for their
    # headlines

    for heads in all_heads:
        full_list.append(heads.get_text())
    return full_list


'''Function used to scrape both the headline and its href link. This function is used as part of the recommender system.
   It returns a list of the full list of headlines and the corresponding links for them.'''


def scrape(word):
    full_list = []
    all_links = []
    ap = 'http://hosted.ap.org/dynamic/external/search.hosted.ap.org/wireCoreTool/Search?SITE=AP&SECTION=HOME' \
         '&TEMPLATE=DEFAULT&query='

    page = urlopen(ap + word)

    soup = BeautifulSoup(page, 'lxml')

    all_heads = soup.find_all('span', {'class': 'latestnews'})
    for a_tag in soup.find_all('a', href=True):
        if a_tag['href'].startswith('/dynamic/stories/'):  # This step is needed to weed out the unwanted links
            all_links.append('http://hosted.ap.org' + a_tag['href'])
    for heads in all_heads:
        full_list.append(heads.get_text())
    return full_list, all_links


'''Function that clears all the contents of all the files in all the directories'''


def clear_everything():
    all_files = get_document_filenames()
    for i in all_files:
        clear_contents(i)


'''Function that clears the contents of one single text file'''


def clear_contents(filename):
    open(filename, 'w').close()


'''Function that explicitly defines a list of lists to match each headline with the corresponding file to dump its
   news text into. Pretty inefficient and ugly. Could probably optimize later with loops'''


def write_text_to_files(headlines_list):
    file_list = [[headlines_list[0], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t1\a1.txt'],
                 [headlines_list[1], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t1\a2.txt'],
                 [headlines_list[2], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t1\a3.txt'],
                 [headlines_list[3], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t2\a1.txt'],
                 [headlines_list[4], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t2\a2.txt'],
                 [headlines_list[5], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t2\a3.txt'],
                 [headlines_list[6], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t3\a1.txt'],
                 [headlines_list[7], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t3\a2.txt'],
                 [headlines_list[8], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t3\a3.txt'],
                 [headlines_list[9], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t4\a1.txt'],
                 [headlines_list[10], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t4\a2.txt'],
                 [headlines_list[11], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t4\a3.txt'],
                 [headlines_list[12], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t5\a1.txt'],
                 [headlines_list[13], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t5\a2.txt'],
                 [headlines_list[14], r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp\t5\a3.txt']]
    for i in range(15):
        with open(file_list[i][1], 'w') as file:
            file.write(file_list[i][0])


'''Function that returns the full news article text for a single link. The AP uses html under the p tag and class
   ap-story-p. Returns a string of the entire article'''


def return_full_news_string(ap):
    full_list = []
    page = urlopen(ap)

    soup = BeautifulSoup(page, 'lxml')

    all_heads = soup.find_all('p', {'class': 'ap-story-p'})
    for heads in all_heads:
        full_list.append(heads.get_text())
    full_list = full_list[0:len(full_list) - 1]
    a = ' '.join(full_list)

    return a


'''Function that clears the recommendations text file and updates it using the top 5 results from the tfidf algorithm'''


def update_recommendations(headlines_list):
    clear_contents(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\docs\topics.txt')
    with open(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\docs\topics.txt', 'w') as file:
        file.writelines("\n".join(headlines_list))

'''Flask ask function that resets the preferences to the initial one. Mainly to simplify the typing'''


@ask.intent('ResetPreferencesIntent')
def reset_preferences():
    update_recommendations(['trump', 'gop', 'military', 'budget', 'new york'])
    return statement('Preferences have been reset')

'''Flask ask function that returns the list from the recommended topics text file'''


@ask.intent('RecommendedTopicsIntent')
def return_topics():
    lines = []
    with open(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\docs\topics.txt') as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    all_topics = '... '.join(lines)
    message = render_template('recommended_topics')
    return statement(message + '... ' + all_topics)


@ask.intent('RecommendedNewsIntent')
def recommended_news():
    lines = []
    '''e = everything. We need a separate list for holding the entire set of 3 news articles in each of the
       5 different topics we are searching for according to the recommendations'''
    e1 = []
    e2 = []
    e3 = []
    e4 = []
    e5 = []

    with open(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\docs\topics.txt') as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    h1, l1 = scrape(lines[0])  # A separate list for each of the top 3 headlines + links from each topic searched
    h2, l2 = scrape(lines[1])
    h3, l3 = scrape(lines[2])
    h4, l4 = scrape(lines[3])
    h5, l5 = scrape(lines[4])
    '''Highly inefficient bit. Goes through each of the 5 different topics' lists and returns and appends each of its
       full article texts to the corresponding list e1, e2, etc. which is itself a list of 3 elements -> one for each
       of the 3 articles in each topic'''
    for a in l1[:3]:
        e1.append(return_full_news_string(a))
    for b in l2[:3]:
        e2.append(return_full_news_string(b))
    for c in l3[:3]:
        e3.append(return_full_news_string(c))
    for d in l4[:3]:
        e4.append(return_full_news_string(d))
    for e in l5[:3]:
        e5.append(return_full_news_string(e))

    write_text_to_files(e1 + e2 + e3 + e4 + e5)  # Write all the lists to their corresponding files
    update_tfidf()  # Probably remove
    all_recommended_headlines_list = list(set(h1[:3] + h2[:3] + h3[:3] + h4[:3] + h5[:3]))  # Adds all the headlines and
    # removes duplicates and saves as a list
    all_recommended_headlines_string = '... '.join(
        all_recommended_headlines_list)  # Converts the list to a large string
    message = render_template('recommended_news')
    return statement(message + '... ' + all_recommended_headlines_string)


'''Flask ask function for searching the ap website for one single term'''


@ask.intent('SearchWordIntent')
def search_news(word):
    if word is None:
        reprompt_word = render_template("reprompt_word")
        return question(reprompt_word)
    else:
        all_heads = parse_word(word)
        latest_news_message = render_template('latest_news', word=word)
        heads = '... '.join(all_heads)
        return statement(latest_news_message + '... ' + heads + '... ')


'''Flask ask function that plays the archival radio'''


@ask.intent('PlayRadioIntent')
def play_radio():
    stream_url = 'https://ia801902.us.archive.org/29/items/AP_NetworkFeed_01-28-85/AP%20Network%20Feed%2001-28-85%20' \
                 '%281%29.ogg '
    return audio('Playing the 1985 archival AP radio about the Challenger disaster').play(stream_url)


'''Flask ask function that pauses the archival radio'''


@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('').stop()


'''Flask ask function that resumes the archival radio'''


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()


'''Flask ask function that stops the archival radio'''


@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)


if __name__ == '__main__':
    app.run(debug=True)
