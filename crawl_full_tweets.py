# coding: utf-8

import twitter
import time
from pymongo import MongoClient
from datetime import datetime
import json









def get_all_tweets(screen_name,tweets_set,earliest_timestamp):
    try:
        tweetList = api.GetUserTimeline(screen_name = screen_name,count=200)
        if len(tweetList)==0:
            return
        tweets_set.insert_many(list(map(lambda x:x.AsDict(),tweetList)))
    except twitter.TwitterError as e:
        print(str(e))
        time.sleep(15 * 60)
        tweetList = api.GetUserTimeline(screen_name = screen_name,count=200)
        tweets_set.insert_many(list(map(lambda x:x.AsDict(),tweetList)))
    oldest = tweetList[-1].id - 1
    if datetime.strptime(tweetList[-1].created_at, "%a %b %d %H:%M:%S +0000 %Y").timestamp()<earliest_timestamp:
        return
    print(screen_name)
    count=len(tweetList)
    while len(tweetList) > 0:
        try:
            tweetList = api.GetUserTimeline(screen_name = screen_name,count=200,max_id=oldest)
            count+=len(tweetList)
        except twitter.TwitterError as e:
            print(str(e))
            time.sleep(60)
            continue
        if len(tweetList)>0:
            tweets_set.insert_many(list(map(lambda x:x.AsDict(),tweetList)))
            oldest = tweetList[-1].id - 1
            if datetime.strptime(tweetList[-1].created_at, "%a %b %d %H:%M:%S +0000 %Y").timestamp()<earliest_timestamp:
                return
        else:
            break








        


def main():
    print("usage: python twitter_crawler consumer_key consumer_secret access_token_key access_token_secret mongodb_ip mongodb_port follower_screennames_json_path")
    consumer_key=sys.argv[1]
    consumer_secret=sys.argv[2]
    access_token_key=sys.argv[3]
    access_token_secret=sys.argv[4]
    mongodb_ip=sys.argv[5]
    mongodb_port=(int)(sys.argv[6])
    follower_screennames_json_path=sys.argv[7]


    api = twitter.Api(consumer_key=consumer_key,
consumer_secret=consumer_secret,
access_token_key=access_token_key,
access_token_secret=access_token_secret,cache=None,tweet_mode= 'extended')

    conn = MongoClient(mongodb_ip, mongodb_port)
    db = conn.top1000full
    tweets_set = db.tweets
    users_set = db.users


    with open(follower_screennames_json_path) as f:
        screen_names=json.loads(f.read())

    start_time = "Thu Mar 1 00:00:00 +0000 2018"
    start_time = datetime.strptime(start_time, "%a %b %d %H:%M:%S +0000 %Y").timestamp()
    index=0
    while index<len(screen_names):
        try:
            screen_name=screen_names[index]
            get_all_tweets(screen_name,tweets_set,start_time)
            print(time.ctime()+":"+screen_name+":"+str(index))
            index+=1
        

        except Exception as e:
            index+=1
            print(str(e))
            continue

if __name__ == '__main__':
    main()