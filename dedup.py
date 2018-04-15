from bson.objectid import ObjectId
from collections import defaultdict
from pymongo import MongoClient

client = MongoClient()

db = client.twitter

tweets = db.tweets
users = db.users

tweet_map = defaultdict(int)
user_map = defaultdict(int)
for tweet in tweets.find():
    tid = tweet['id']
    _id = tweet['_id']
    tweet_map[tid] += 1
    if tweet_map[tid] > 1:
        result = tweets.delete_one({'_id': ObjectId(_id)})

for user in users.find():
    uid = user['id']
    _id = user['_id']
    user_map[uid] += 1
    if user_map[uid] > 1:
        result = tweets.delete_one({'_id': ObjectId(_id)})
