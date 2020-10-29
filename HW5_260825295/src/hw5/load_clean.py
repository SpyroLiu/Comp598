import json
from datetime import datetime

def get_post_list(path):
    all_post = []
    with open(path, 'r') as f:
        for line in f:
            try:
                temp = json.loads(line)
                all_post.append(temp)
            except json.decoder.JSONDecodeError:
                pass
    return all_post


def title_check(post_list):
    all_post = post_list
    all_post = [x for x in all_post if 'title' in x['data'] or 'title_text' in x['data']]
    for i in all_post:
        if 'title_text' in i['data']:
            i['data']['title'] = i.pop('title_text')
    return all_post


def time_standardize(post_list):
    all_post = post_list
    new_post = []
    for i in all_post:
        if 'createdAt' not in i['data']:
            new_post.append(i)
            continue
        temp = i['data']['createdAt']
        try:
            if temp[-3] != ':':
                k = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S%z")
            else:
                temp = temp[:-2] + ':' + temp[-2:]
                k = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S%z")
            i['data']['createdAt'] = k.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            new_post.append(i)
        except ValueError:
            pass

    return new_post
