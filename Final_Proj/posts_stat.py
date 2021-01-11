import pandas as pd
import random
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
from collections import Counter
import json
import os
from collections import OrderedDict
import sys

def merge_df(df1, df2):
    return pd.concat([df1,df2])

def psedo_topics(df,topics):
    df['topics'] = [random.choice(topics) for _ in range(1000)]
    return df

def count_words(df,topic):
    str_topic = ' '.join(list(df['title'][df['topics'] == topic])).lower()
    # Remove non-alphabetic part
    regex = re.compile('[^a-zA-Z]')
    str_topic = regex.sub(' ',str_topic)
    str_topic = nltk.word_tokenize(str_topic)
    # Lemmatize all words
    lemmatizer = nltk.stem.WordNetLemmatizer()
    str_topic = [lemmatizer.lemmatize(x,pos = 'v') for x in str_topic]
    # Remove stop word
    str_topic = [w for w in str_topic if w not in stopwords.words('English')]
    return Counter(str_topic)

def tfidf_calculate(tp,dataset,num=10):
  word_tfidf={}
  for word in tp:
    tf = tp[word] / sum(tp.values())
    num_topics = 0
    for k, v in dataset.items():
      if word in v.keys():
          num_topics = num_topics + 1
    all_topics = 9
    idf = np.log(all_topics / num_topics)
    tfidf = tf * idf
    word_tfidf[word] = round(tfidf,5)
  return Counter(word_tfidf).most_common(num)

def convert_to_str_percent(counter):
    ct = dict(counter)
    del ct['other']
    result = {}
    nums_total = sum(ct.values())
    for k,v in ct.items():
        result[k] = round(ct[k]/nums_total,5)
    return str(result)

def convert_to_str_percent_sp(counter):
    ct = dict(counter)
    result = {}
    nums_total = sum(ct.values())
    for k,v in ct.items():
        result[k] = round(ct[k]/nums_total,5)
    return str(result)

if __name__ == '__main__':
    topics = ['cov', 'par', 'pub', 'ele', 'cou', 'tru', 'bid', 'ank','other']
    topics8 = ['cov', 'par', 'pub', 'ele', 'cou', 'tru', 'bid', 'ank']
    topics_wordcount = dict.fromkeys(topics,None)

    c1 = pd.read_csv('/Users/tylerliu/GitHub/Comp598/Final_Proj/candi/conservatives_hot_updated.csv',sep='^',
                     error_bad_lines=False)
    c2 = pd.read_csv('/Users/tylerliu/GitHub/Comp598/Final_Proj/n_candi/conservatives_hot_no_mention_updated.csv',sep='^',
                     error_bad_lines=False)
    c2['topics'] = ['other']*len(c2)
    c = merge_df(c1,c2)

    p1 = pd.read_csv('/Users/tylerliu/GitHub/Comp598/Final_Proj/candi/politics_hot_updated.csv',sep='^',
                     error_bad_lines=False)
    p2 = pd.read_csv('/Users/tylerliu/GitHub/Comp598/Final_Proj/n_candi/politics_hot_no_mention_updated.csv',sep='^',
                     error_bad_lines=False)
    p2['topics'] = ['other'] * len(p2)
    p = merge_df(p1,p2)

    ap = merge_df(c,p)
    trump_mention = ap['title'].str.contains('Donald|Trump',case = False)
    biden_mention = ap['title'].str.contains('Joe|Biden',case = False)
    # Here we obtain a dict with the Counter as the value
    for t in topics:
        topics_wordcount[t] = dict(count_words(ap,t))
    # Get tf-idf score
    topics_tfidf = dict.fromkeys(topics8, None)
    for tp in topics8:
        topics_tfidf[tp] = OrderedDict(tfidf_calculate(topics_wordcount[tp], topics_wordcount,num=10))

    with open(os.getcwd()+'/summary','w') as f:
        f.write('The top 10 tf-idf score under each topic is:\n')
        result = json.dumps(topics_tfidf, indent=2)
        f.write(result)
        f.write('\n\nThe topic distribution is (\'other\' is included in integer form):\n')
        f.write(str(Counter(ap['topics'])))
        f.write('\n\nThe % topic distribution is (\'other\' is excluded):\n')
        f.write(convert_to_str_percent(Counter(ap['topics'])))
        f.write('\nThe % topic distribution from subreddit \'politics\' is:\n')
        f.write(convert_to_str_percent(Counter(p['topics'])))
        f.write('\nThe % topic distribution from subreddit \'conservatives\' is:\n')
        f.write(convert_to_str_percent(Counter(c['topics'])))
        f.write('\n\n')

        f.write('\nThe % topics distribution for posts concerned with Trump is:\n')
        f.write(convert_to_str_percent_sp(Counter(np.asarray(ap['topics'])[trump_mention])))
        f.write('\nThe % topics distribution for posts concerned with Biden is:\n')
        f.write(convert_to_str_percent_sp(Counter(np.asarray(ap['topics'])[biden_mention])))

