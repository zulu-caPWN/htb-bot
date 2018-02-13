#can get rid of prev version post_to_twitter.py

from time import sleep
import requests
from pymongo import MongoClient
import tweepy
from pymongo import ReturnDocument
import htb_sensitive

######
# DB #
######
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.htb #db name
cursor = db.htb #collection name
print htb_sensitive.mongopath

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

num_posted = 0
num_unposted = 0
more_to_post = True

while more_to_post == True:
    #####################
    # TWITTER CONSTANTS #
    #####################
    #HTB twitter
    available_length = 280
    htb_twitter = '@hackthebox_eu '
    htb_twitter_length = len(htb_twitter)

    pre_counter = 1
    post_counter = 1
    counter_msg = str(pre_counter) + '/' + str(post_counter) + '\n'
    counter_msg_length = len(counter_msg) + 1
    available_length -= counter_msg_length

    available_length -= htb_twitter_length
    print 'Avail length, with only htb twitter acct is', available_length
    count_list = []

    test = 'this is a test'
    to_twitter = ''
    to_twitter += htb_twitter
    #to_twitter += counter_msg
    to_twitter += '\n'

    ###############################
    # GET FROM DB, LOOP & PROCESS #
    ###############################
    retrieve = cursor.find({'to_twitter':0})
    for i in retrieve:
        msg_length = i['msg_length'] + 1 #to add \n
        available_length -= msg_length
        #available_length -= i['msg_length']

        print 'length of this msg is', i['msg_length']
        print 'available characters after this msg is', available_length

        if available_length >= 0:
            count_list.append(i['_id'])
            print 'added', i['raw_msg']
            print
            to_twitter += i['raw_msg']
            to_twitter += '\n'
            num_posted += 1

        else:
            print '####################################'
            print 'not enuff space to add', i['raw_msg']
            print
            num_unposted += 1

    print 'Posting %d' %num_posted
    print 'Unposted %d' % num_unposted

    if num_unposted != 0:
        more_to_post = True
    else:
        more_to_post = False

    #print to_twitter
    prepped = to_twitter.decode('unicode_escape').encode('ascii', 'ignore')
    sleep(1)

    if num_posted >= 1:
        try:
            update = api.update_status(prepped)
            print 'Posted to Twitter \n', update
            sleep(1)
        except tweepy.TweepError as e:
            print e.reason
            sleep(1)
    else:
        print 'We have nothing to post to twitter'

    ###############################
    # UPDATE DB WITH POSTED MSG'S #
    ###############################
    print 'Marking DB entries as to_twitter:1'
    for i in count_list:
        print i
        p =cursor.find_one_and_update({'_id': i},
                                   {'$set': {'to_twitter': 1}},
                                   return_document=ReturnDocument.AFTER)
        #print p

    num_posted = 0
    num_unposted = 0

print 'All Done'
