# coding: utf-8

import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
import time
import json
import sys
from __future__ import unicode_literals



def get_all_tweets(screen_name):
    try:
        tweetList = api.user_timeline(screen_name = screen_name,count=200)
        if len(tweetList)==0:
            return
        tweets_set.insert_many(list(map(lambda x:x._json,tweetList)))
    except tweepy.RateLimitError:
        time.sleep(15 * 60)
        tweetList = api.user_timeline(screen_name = screen_name,count=200)
        tweets_set.insert_many(list(map(lambda x:x._json,tweetList)))
    oldest = tweetList[-1].id - 1
    
    count=len(tweetList)
    while len(tweetList) > 0:
        try:
            tweetList = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
            count+=len(tweetList)
        except tweepy.RateLimitError:
            time.sleep(60)
            continue
        if len(tweetList)>0:
            tweets_set.insert_many(list(map(lambda x:x._json,tweetList)))
            oldest = tweetList[-1].id - 1
        else:
            break



def main():
    print("usage: python twitter_crawler consumer_key consumer_secret access_token_key access_token_secret mongodb_ip mongodb_port follower_ids_json_path")
    consumer_key=sys.argv[1]
    consumer_secret=sys.argv[2]
    access_token_key=sys.argv[3]
    access_token_secret=sys.argv[4]
    mongodb_ip=sys.argv[5]
    mongodb_port=(int)(sys.argv[6])
    follower_ids_json_path=sys.argv[7]
    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)

    conn = MongoClient(mongodb_ip, mongodb_port)
    db = conn.twitter
    tweets_set = db.tweets
    users_set = db.users


    with open(follower_ids_json_path) as f:
        all_follower_ids=json.loads(f.read())

    batch=100
    limit=100000
    for i in range(0,limit,batch):
        batch_user_list=all_follower_ids[i:i+batch]
    users = api.lookup_users(user_ids=batch_user_list)
    users_set.insert_many(list(map(lambda x:x._json,users)))
    for index,user in enumerate(users):
        if not user.protected:
            get_all_tweets(user.screen_name)
        print(time.ctime()+":"+user.screen_name+":"+str(i+index))





if __name__ == '__main__':
    main()



