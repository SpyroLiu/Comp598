import requests
import argparse
import json
import sys
import os.path as osp
dir_name = osp.dirname(__file__)

def get_post(subreddit_name):
    final_data =[]
    after = ''
    for i in range(0,5):
        data,after = iter_after(subreddit_name,after)
        final_data = final_data + data
    return final_data

def iter_after(subreddit_name,after):
    if not after:
        data = requests.get(f'http://api.reddit.com{subreddit_name}/new?limit=100',
                            headers={'User-Agent': 'windows:requests (by /u/tylerliu)'})
        data = data.json()['data']['children']
    else:
        data = requests.get(f'http://api.reddit.com/{subreddit_name}/hot?limit=100&after={after}',
                            headers={'User-Agent': 'windows:requests (by /u/tylerliu)'})
        data = data.json()['data']['children']
    after = data[-1]['data']['name']
    return data,after

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help = 'The output file path')
    parser.add_argument('subreddit', help = 'The subreddit to collect data from')
    args = parser.parse_args()
    if not args.o or not args.subreddit:
        print("Incomplete input!")
        sys.exit()
    k = get_post(args.subreddit)
    save_path = osp.join(dir_name,'..','data',args.o)
    with open(save_path,'w',encoding='utf-8') as f:
        for i in k:
            f.write(json.dumps(i))
            f.write('\n')