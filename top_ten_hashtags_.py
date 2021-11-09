import json
import re
import sys


##########-----------------------------------------------------##########

def extract_tweet():
    # loading the tweet streaming data into a list of dictionaries
    raw_tweet_data = []

    with open(sys.argv[1]) as read_file:
        for line in read_file:
            tweetr = json.loads(line)
            raw_tweet_data.append(tweetr)

    # extracting the raw text
    return raw_tweet_data


def extract_hashtags(raw_tweet_data):
    # extract hashtag text(s) from each tweet and store them in a list, without sorting or counting yet

    hashtag_dict = []
    for line in raw_tweet_data:
        if len(line) != 1 and line['entities']['hashtags'] != []:
            hashtag_dict.append(line['entities']['hashtags'])

    hashtag_list = []
    for line in hashtag_dict:
        for item in line:
            hashtag_list.append(item['text'])

    return hashtag_list


##########-----------------------------------------------------##########

def top_ten_hashtags(hashtag_list):
    # count, sort, and print 10 top hashtags

    # (1) counting
    hashtag_count = {}  # hashtag:count dictionary
    for hashtag in hashtag_list:
        if hashtag not in hashtag_count.keys():
            hashtag_count[hashtag] = 1
        else:
            hashtag_count[hashtag] += 1

    # (2) sorting hashtag:count dict -> a list of (hashtag:count) tuples
    sorted_hashtags = sorted(hashtag_count.items(), key=lambda x: x[1], reverse=True)

    # (3) printing the top 10 hashtags
    top_ten = sorted_hashtags[0:10]
    for hashtag in top_ten:
        print(str(hashtag[0]) + ' ' + str(hashtag[1]))

##########-----------------------------------------------------##########

if __name__ == '__main__':

    raw_tweet = extract_tweet()
    hashtag_list = extract_hashtags(raw_tweet)
    top_ten_hashtags(hashtag_list)
