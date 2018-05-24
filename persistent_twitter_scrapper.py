# Import the Twython class
from twython import Twython, TwythonStreamer
import json
# import pandas as pd
import csv
import datetime
from requests.exceptions import *


def process_tweet(tweet):
    # Filter out unwanted data
    d = {}
    d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    try:
        for key in {
		    'created_at', 'id', 'text', 'source', 'truncated', 
            'in_reply_to_status_id', 'in_reply_to_user_id',
            'in_reply_to_screen_name', 'user', 'coordinates',
            'place', 'quoted_status_id', 'is_quote_status', 'quoted_status',
            'retweeted_status', 'quote_count', 'reply_count', 'retweet_count',
            'favorite_count', 'favorited', 'retweeted', 'entities', 'extended_entities',
            'possibly_sensitive', 'filter_level', 'lang', 'matching_rules'}:
            if key == 'user':
                    pass
            elif key == 'place':
                    pass
            elif key == 'quoted_status' or key == 'retweeted_status':
                    pass
            elif key == 'entities':
                    pass
            elif key == 'extended_entities':
                    pass
            else:
                    d[key] = tweet[key]

    except KeyError as e:
        pass
    # d['text'] = tweet['text']
    # d['user'] = tweet['user']['screen_name']
    # d['user_loc'] = tweet['user']['location']
    # d['date'] = tweet['created_at']
    return d


# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):

    # Received data
    def on_success(self, data):

        # # Only collect tweets in English
        # if data['lang'] == 'en':
        # tweet_data = process_tweet(data)
        print(datetime.datetime.now())
        # self.save_to_csv(tweet_data)
        self.save_to_json(data)

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    # Save each tweet to csv file
    def save_to_csv(self, tweet):
        # with open(r'saved_tweets.csv', 'a') as out_file:
        with open(r'saved_tweets_big.csv', 'a') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(list(tweet.values()))
    def save_to_json(self, tweet):
        with open('saved_tweets_big.json', 'a') as out_file:
            json.dump(tweet, out_file)

def main():

    # Load credentials from json file
    with open("twitter_credentials.json", "r") as tw_creds:
        creds = json.load(tw_creds)

    # Instantiate an object
    # python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    while True:
        try:
            # Instantiate from our streaming class
            stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                                creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
            # Start the stream
            # stream.statuses.filter(track='madrid')
            stream.statuses.filter(locations='-7.876154,37.460012,3.699873,43.374723')
        except ConnectionError as e:
            print(e)

if __name__ == "__main__":
    main()
