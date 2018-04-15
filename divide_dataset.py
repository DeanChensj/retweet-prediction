import random
from datetime import datetime
from pymongo import MongoClient

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

    # Extract selected attributes
    user = tweet['user']
    f_user = {'id': user['id'], 'name': user['name'], 'screen_name': user['screen_name'], 'verified': user['verified'],
              'followers_count': user['followers_count'], 'friends_count': user['friends_count'],
              'listed_count': user['listed_count']}

    features = {'created_at': tweet['created_at'], 'id': tweet['id'], 'text': tweet['text'],
                'entities': tweet['entities'], 'user': f_user, 'retweet_count': tweet['retweet_count']}

    # Divide data set
    rand = random.randint(1, 101)
    if rand <= 80:
        train.insert_one(features)
    elif rand <= 90:
        valid.insert_one(features)
    else:
        test.insert_one(features)
