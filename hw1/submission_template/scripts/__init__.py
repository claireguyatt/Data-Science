import pandas as pd
import re

# read the data into a pandas dataframe (only first 10,000 tweets)

tweets = pd.read_csv("data/IRAhandle_tweets_1.csv", nrows=10001)

# remove non English & question tweets

tweets = tweets[tweets.language == "English"]
tweets = tweets[tweets.content.str.contains("\?")==False]

# create new tsv file w/ refined data set

tweets.to_csv('dataset.tsv', sep='\t', index=False)

# add boolean feature for if tweet contains word Trump & set accordingly

tweets["trump_mention"] = False
tweets.loc[tweets.content.str.contains("\WTrump\W"), 'trump_mention'] = True

# make data set w/ added feature & right columns in right order

annotated_data = tweets[['tweet_id', 'publish_date', 'content', 'trump_mention']]
annotated_data.to_csv('dataset.tsv', sep='\t', index=False)

# compute % tweets containing word Trump & put in tsv

total_tweets = len(annotated_data.index)
trump_tweets = annotated_data.trump_mention.value_counts()[True]
percent_trump = round(trump_tweets/total_tweets, 3)

# create new tsv with results

data = { 'result': ['frac_trump_mentions'], 'value': [percent_trump] }
result = pd.DataFrame(data, columns = ['result', 'value'])
result.to_csv('results.tsv', sep='\t', index=False)








