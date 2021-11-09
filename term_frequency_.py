import json
import re
import sys


##########---------- PROCESSING TWEET STREAMING DATA ----------##########

# MAIN - loading raw tweet json file and extracting the text from each tweet, returning list of raw texts
def extract_tweet():
    # loading the tweet streaming data into a list of dictionaries
    raw_tweet_data = []

    with open(sys.argv[1]) as read_file:
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
    raw_text = []   # a list to contain the raw text from every single tweet data. Texts from deleted tweets will be stored as string 'deleted tweet'. AFINN-111.txt contains none of those words
    for line in raw_tweet_data:
        if len(line) == 1:
            raw_text.append('deleted tweet')
        else:
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


##########------------------ TERM FREQUENCIES -----------------##########

def count_term_frequency(tweet_list):
    term_count = {}         # {term:count}
    all_term_count = 0      # total number of words in all tweets

    for tweet in tweet_list:
        words = tweet.split()   # split each tweet into list of [words]
        normalized_words = [word.strip().lower() for word in words]

        for term in normalized_words:
            all_term_count += 1

            if term not in term_count.keys():
                term_count[term] = 1
            else:
                term_count[term] += 1

    # transform the term_count dict to term:frequency
    term_frequency = {term: count/all_term_count for term, count in term_count.items()}

    return term_frequency

##########-----------------------------------------------------##########

if __name__ == '__main__':

    raw_text_ = extract_tweet()
    cleaned_text = clean_tweet(raw_text_)
    term_frequency = count_term_frequency(cleaned_text)

    for term in term_frequency.keys():
        print(str(term) + ' ' + str(term_frequency[term]))
