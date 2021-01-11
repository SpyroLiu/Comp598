import json
import random
import pandas as pd
import os.path as osp
import os

dir_name = os.getcwd()


# dir_name = osp.dirname(__file__)
def load_json(date, p_or_c, h_or_new):
    path_list = [osp.join(dir_name, 'data', '2020' + d + '_' + p_or_c + '_' + h_or_new + '.json') for d in date]
    ls = []
    for p in path_list:
        with open(p, 'r', encoding='utf-8') as f:
            for l in f:
                k = json.loads(l)['data']['title']
                ls.append(k)
    return ls


def filter_candi(posts):
    p = list(set(posts))
    p = random.sample(p, 1000)
    p = p[:1000]
    name_ls = ['donald', 'trump', 'joe', 'biden']
    p = list([x for x in p if any(n in x.lower() for n in name_ls)])
    return p


def filter_n_candi(posts, num):
    p = list(set(posts))
    name_ls = ['donald', 'trump', 'joe', 'biden']
    p = list([x for x in p if not any(n in x.lower() for n in name_ls)])
    p = random.sample(p, num)
    return p


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    date = ['1130', '1201', '1202']

    # p_h = load_json(date, 'politics', 'hot')
    # p_h_f = filter_candi(p_h)
    # len(p_h_f)
    # c_h = load_json(date, 'conservative', 'hot') + load_json(date, 'conservative', 'new')[0:800]
    # c_h_f = filter_candi(c_h)
    # len(c_h_f)
    # assign1 =  ['GW'] * (300 - len(c_h_f) + 90 ) + ['CJ'] * (len(p_h_f)-(300 - len(c_h_f) + 90 ))
    # p_h_f_df = pd.DataFrame({'who':assign1, 'title':p_h_f, 'topics':['']*len(p_h_f),})
    # p_h_f_df.to_csv(os.getcwd()+osp.sep+'politics_hot_updated.csv', sep="\t", index=False)
    #
    # assign2 = ['LJ'] * 90 + ['GW'] * (len(c_h_f)-90)
    # c_h_f_df = pd.DataFrame({'who':assign2, 'title':c_h_f, 'topics':['']*len(c_h_f)})
    # c_h_f_df.to_csv(os.getcwd()+osp.sep+'conservatives_hot_updated.csv', sep="\t", index=False)

    p_h = load_json(date, 'politics', 'hot')
    p_h_nf = filter_n_candi(p_h, 390)
    c_h = load_json(date, 'conservative', 'hot')
    c_h_nf = filter_n_candi(c_h, 770)
    p_h_nf_df = pd.DataFrame({'who': ['NA'] * 390, 'title': p_h_nf, 'topics': ['NA'] * 390})
    p_h_nf_df.to_csv(os.getcwd() + osp.sep + 'politics_hot_no_mention_updated.csv', sep="\t", index=False)
    c_h_nf_df = pd.DataFrame({'who': ['NA'] * 770, 'title': c_h_nf, 'topics': ['NA'] * 770})
    c_h_nf_df.to_csv(os.getcwd() + osp.sep + 'conservatives_hot_no_mention_updated.csv', sep="\t", index=False)
