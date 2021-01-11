import requests
import json
import os.path as osp

def get_posts(subreddit_name):
    data = requests.get(f'http://api.reddit.com/r/{subreddit_name}/new?limit=500', headers ={'User-Agent': 'windows:requests (by /u/tylerliu)'})
    data = data.json()['data']['children']
    return data

def get_post_samples():
    dir = osp.dirname(__file__)
    p1 = osp.join(dir,'..','..','data','sample1.json')
    p2 = osp.join(dir, '..', '..', 'data', 'sample2.json')
    l1 = ['funny','AskReddit','gaming','aww','pics','Music','science','worldnews','videos','todayilearned']
    l2 = ['AskReddit','memes','politics','nfl','nba','wallstreetbets','teenagers','PublicFreakout','leagueoflegends','unpopularopinion']

    sample1 = []
    for sub in l1:
        sample1 = sample1 + get_posts(sub)
    with open(p1,'w',encoding='utf-8') as f:
        for p in sample1:
            f.write(json.dumps(p))
            f.write('\n')

    sample2 = []
    for sub in l2:
        sample2 = sample2 + get_posts(sub)
    with open(p2,'w',encoding='utf-8') as f:
        for p in sample2:
            f.write(json.dumps(p))
            f.write('\n')