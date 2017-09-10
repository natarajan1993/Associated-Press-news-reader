# AP_scraper

A rough implementation of an Alexa skill using flask-ask, beautiful soup and scikit-learn. The machine learning
algorithm used for updating the user preferences is called tf-idf (Term Frequency-Inverse Document Frequency. It
looks through a set of documents and finds the most common words among all the documents and ranks them by their
frequency scores. Right now the machine learning itself is very slow because it's trawling through a set of docs on
the local machine. More development is needed to optimize and streamline the process. Each document contains a single
article scraped directly from the html using beautiful soup which is also very slow. Maybe with an API key, the
article scraping can be very easily streamlined. Also, while tfidf is a the industry standard, there must be a
separate machine learning and training algorithm for implementing machine learning using the AP's metadata tagging
system.

 The app can do the following:
 1. Search for a term and return the headlines related to that
 2. Use the text from the top 3 headlines in 5 separate preferences to learn the user's preferences and update
 the in-built preference accordingly. The user can set initial preferences
 3. Play an archival recording of the AP's coverage of the 1985 Challenger disaster
 4. Summarize a headline's text
 
 Developed by:
 Natarajan Mahalingam
 2017 Crosby MBA Spring Entry
 University of Missouri, Columbia
 April, 2017
