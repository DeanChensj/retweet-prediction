import random
from datetime import datetime
from pymongo import MongoClient
random.seed(2018)

client = MongoClient()
db = client.twitter
tweets = db.tweets
users = db.users

# Create db / collections for train / test / valid
db = client.project
train = db.train
valid = db.valid
test = db.test

start_time = "Thu Mar 1 00:00:00 +0000 2018"
start_time = datetime.strptime(start_time, "%a %b %d %H:%M:%S +0000 %Y")

for tweet in tweets.find():
    # Select tweet according to timestamp
    timestamp = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
    if timestamp < start_time:
        continue
    # Only tweets in English
    if tweet['lang'] != 'en':
        continue
    

    # Divide data set
    rand = random.randint(1, 101)
    if rand <= 80:
        train.insert_one(tweet)
    elif rand <= 90:
        valid.insert_one(tweet)
    else:
        test.insert_one(tweet)
