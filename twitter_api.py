#testing connection to twitter api

import tweepy
import time
from pymongo import MongoClient
import htb_sensitive

###################
# INSTANTIATE API #
###################
consumer_key = htb_sensitive.consumer_key
consumer_secret = htb_sensitive.consumer_secret
access_token = htb_sensitive.access_token
access_token_secret = htb_sensitive.access_token_secret
auth= tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

###########
# DB INFO #
###########
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.twitterDB  # db name
cursor = db.scraped_users  # collection name


api.update_status('Hello World')