import json
import re
import sys


##########---------- PROCESSING TWEET STREAMING DATA ----------##########

# MAIN - loading raw tweet json file and extracting the text from each tweet, returning list of raw texts
def extract_tweet():
    # loading the tweet streaming data into a list of dictionaries
    raw_tweet_data = []

    with open(sys.argv[2]) as read_file:
        for line in read_file:
            tweetr = json.loads(line)
            raw_tweet_data.append(tweetr)

    # extracting the raw text
    return extract_text(raw_tweet_data)


# cleaning tweets, spplying cleantxt(), returning list of cleaned texts
def clean_tweet(raw_text):
    clean_text_map = map(cleantxt, raw_text)
    return list(clean_text_map)


# function to extract the text from the raw tweet data, returning list of raw texts
def extract_text(raw_tweet_data):
    raw_text = []   # a list to contain the raw text from raw tweet data. Texts from non-english and deleted tweets are filtered out
    for line in raw_tweet_data:
        if len(line) != 1:
            raw_text.append(line['text'])

    return raw_text

# emoji patterns to be removed
emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)


# function to clean texts
def cleantxt(text):
    text = re.sub(r'https?:\/\/\S+', ' ', text)          # remove links
    text = re.sub(r'https?:\S+', ' ', text)              # remove links
    text = re.sub(r'@[A-Za-z0-9_:]+', ' ', text)         # remove mentions
    text = re.sub(r'RT[\s]+', ' ', text)                 # remove RTs
    text = re.sub(r'[\n]', ' ', text)                    # remove '\n'
    text = re.sub(r'[.,:;\"?|\-!#\(\)\[\]]', ' ', text)  # remove hashtags and punctuations
    text = re.sub(r'[\+\/]', ' ', text)                  # remove more punctuations
    text = re.sub(r'&amp', ' ', text)
    text = emoji_pattern.sub(r' ', text)      # remove emojis
    return text


##########-----------------------------------------------------##########

##########--------------- LOADING AFINN SCORES ----------------##########

def load_afinn():
    # loading AFINN scores
    afinn = open(sys.argv[1])

    # dictionary to store term:score data
    scores = {}
    for line in afinn:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    return scores

##########-----------------------------------------------------##########

##########----------------- SENTIMENT SCORING -----------------##########

# the sentiment analysis function
def term_sentiment_analysis(tweet_list, scores):
    term_dict = {} # a dict to contain the non-sentiment

    for tweet in tweet_list:
        score = 0               # a variable to assign the total score to
        words = tweet.split()   # split each tweet into list of [words]
        normalized_words = [word.strip().lower() for word in words]

        # ['this', 'is', 'a', 'tweet'. 'example']

        # calculating the total score
        for term in normalized_words:
            if term in scores.keys():
                score = score + scores[term]
            else:
                score = score + 0

        # filtering the non-sentiment terms
        for term in normalized_words:
            if term in term_dict.keys():
                term_dict[term] = term_dict[term] + score
            else:
                term_dict[term] = score

    return term_dict

##########-----------------------------------------------------##########

if __name__ == '__main__':

    scores = load_afinn()
    raw_text_ = extract_tweet()
    cleaned_text = clean_tweet(raw_text_)
    term_sentiment = term_sentiment_analysis(cleaned_text, scores)

    for key in term_sentiment.keys():
        print(str(key) + ' ' + str(term_sentiment[key]))
