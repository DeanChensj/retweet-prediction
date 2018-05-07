# retweet-prediction
Final project of CMU 15688.
- report.ipynb: the ipython notebook of our report
- SIF_embedding.py: a small library for generating [SIF sentence embedding](https://github.com/PrincetonML/SIF/tree/master/src)
- data_io.py: a script providing data preprocessing for generating SIF sentence embedding
- crawl_full_tweets.py: a crawler script for crawling tweets with full text (note that by default the crawled tweets will be truncated) and store to local mongodb
- generate_dataset.py: a script for generating the train and test dataset jsons
- top_1000_users_screen_names.json: the screen names list json for [top 1000 users with most followers](http://twitaholic.com/top100/followers/)
- kmeans.py: an implementation for kmeans model
- natual_language_processing.py: an implementation for n-gram language model
