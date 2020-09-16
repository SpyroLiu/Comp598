import os
import numpy as np
import pandas as pd
df = pd.read_csv('/Users/tylerliu/GitHub/Comp598/HW_1/IRAhandle_tweets_1.csv', delimiter=',',nrows=10000)
df = df[0:9999]
df = df[df["language"] == 'English']
df = df[-df["content"].str.contains("\?")]
trump_mention = df["content"].str.contains("(?<!\w)Trump(?!\w)|-Trump(?!\w)")
df["trump_mention"] = trump_mention
df.to_csv('new_file.tsv', sep='\t', index=False)

percent = sum(trump_mention)/len(trump_mention)

df_check = df[["content","tweet_id","trump_mention","retweet"]]
df_check = df_check[df_check["trump_mention"] == True]
df_check.to_csv('check_update.csv', sep='\t', index=False)


ds = df[["tweet_id","publish_date","content","trump_mention"]]
ds.to_csv('dataset.tsv', sep='\t', index=False)

result = pd.DataFrame({'result': ['frac-trump-mentions'],'value': ['{:.3%}'.format(percent)]})
result.to_csv('result.tsv', sep='\t',index=False)