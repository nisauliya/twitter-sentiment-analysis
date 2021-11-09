# twitter-sentiment-analysis
This is a collection of scripts I submitted to complete Data Manipulation at Scale (Coursera) by the University of Washington. It's my first time working with real-world data :)  here is the link to the course : https://www.coursera.org/learn/data-manipulation/home/welcome

# the scripts (and what they do):
1. tweet_sentiment__.py (takes tweet streaming data in JSON format and prints out the sentiment score for each tweet)
2. term_sentiment_1.py (also takes raw tweet streaming data in JSON format and prints out the estimated sentiment score for all non-sentiment enducing terms (the ones not listed in AFINN-111.txt). Each non-sentiment word takes the total sentiment score of the tweet it is in as its own score.)
3. term_frequency_.py (same input as above, prints out the frequency of each word in the entire tweet input)
4. top_ten_hashtags_.py (same input as above, prints out the ten top hashtags mentioned)

The sentiment estimations were done using AFINN-111 scores as reference. The very basic sentiment analysis indeed :')
Twitter streaming data were collected using Tweepy.
