# coding: utf-8
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import numpy as np





client = MongoClient('127.0.0.1', 27017)
db = client.top1000full
train = db.tweets





all_tweets=train.find(filter={"lang":"en"},projection=["full_text","retweet_count","user.screen_name","retweeted_status","created_at","user_mentions","urls","hashtags","media"])




tweets_list=[{"text":x["full_text"],"retweet_count":x["retweet_count"] if "retweet_count" in x else -1,"screen_name":x["user"]["screen_name"],
              "has_media":True if "media" in x else False,
                "retweeted":True if "retweeted_status" in x else False, "created_at":x["created_at"],"entities":{"hashtags":x["hashtags"],
                "user_mentions":x["user_mentions"],"urls":x["urls"]}}  for x in all_tweets]




df=pd.DataFrame(tweets_list)
df=df[df["has_media"]==False]
df=df[df["retweeted"]==False]
df=df[df["retweet_count"]>=0]






start_time = "Thu Apr 10 00:00:00 +0000 2018"
start_time = datetime.strptime(start_time, "%a %b %d %H:%M:%S +0000 %Y")
df["time"]=df["created_at"].apply(lambda x:datetime.strptime(x, "%a %b %d %H:%M:%S +0000 %Y"))
all_df=df
train_df=all_df[all_df["time"]<start_time]
test_df=all_df[all_df["time"]>=start_time]

df=train_df
median_s=df.groupby("screen_name").apply(lambda x:np.median(x["retweet_count"]))
median_df=pd.DataFrame({"screen_name":median_s.index.values,"retweet_median":median_s.values})

merged_df=pd.merge(df,median_df,on="screen_name",how="left")
merged_test_df=pd.merge(test_df,median_df,on="screen_name",how="left")
merged_test_df.retweet_median.count()
merged_test_df=merged_test_df.dropna()


merged_df.to_json("train_original_tweets_top1000full_text_only.json")
merged_test_df.to_json("test_original_tweets_top1000full_text_only.json")

