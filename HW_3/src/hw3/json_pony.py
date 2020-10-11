import pandas as pd
import numpy as np
from collections import Counter
import copy
import re
import json
import math

def create_json_pony(src_file, dictionary_for_checking):

    dt = pd.read_csv(src_file, delimiter= ',')
    dt = preprocess(dt)
    pony_analysis = {'verbosity':{}, 'mentions':{}, 'follow_on_comments':{}, 'non_dictionary_words':{}}

    verb = pony_analysis.get("verbosity")
    getVerb(dt,verb)

    ment = pony_analysis.get('mentions')
    getMention(dt,ment)

    foll = pony_analysis.get('follow_on_comments')
    getFoll(dt,foll)

    non_dict = pony_analysis.get('non_dictionary_words')
    getNon_dict(dt,non_dict,dictionary_for_checking)

    # print(pony_analysis)
    analysis_result = json.dumps(pony_analysis, indent=2)
    return analysis_result

    return pony_analysis

def words_cleanning(dialog):
    return re.sub(r'\W+', ' ', dialog)

def UnicodeToSpace(my_str):
    return re.sub(r'\d+', '', my_str)

def is_non_pony(x):
    if x != 'Twilight Sparkle' and x != 'Applejack' and x != 'Rarity' and x != 'Pinkie Pie' and x != 'Rainbow Dash' \
            and x != 'Fluttershy':
        return 'non_Pony'
    else:
        return x

def preprocess(dt):
    eps = dt['title'].unique()
    dt_eps = [dt[dt['title'] == title] for title in eps]
    a = []
    b = []
    index = -1;
    for sub_dt in dt_eps:
        prev_pony = ''
        for id,row in sub_dt[['pony','dialog']].iterrows():
            if row['pony'] != prev_pony:
                a.append(row['pony'])
                b.append(row['dialog'])
                index = index + 1
                prev_pony = row['pony']
            else:
                b[index] = b[index] + ' ' + row['dialog']
    dt = pd.DataFrame({'pony' : a, 'dialog' :b})
    return dt

def getVerb(dt,verb):
    # verbosity
    pony_name = {'twilight': 'Twilight Sparkle', 'applejack': 'Applejack', 'rarity': 'Rarity', 'pinkie': 'Pinkie Pie',
                 'rainbow': 'Rainbow Dash', 'fluttershy': 'Fluttershy'}

    for name, full_name in pony_name.items():
        verb[name] = sum(dt['pony'].str.lower() == str.lower(full_name))
    total_count = sum(verb.values())
    for name, full_name in pony_name.items():
        verb[name] = round(verb[name] / total_count, 2)

def getMention(dt,ment):
    # mentions
    pony_name = {'twilight': 'Twilight Sparkle', 'applejack': 'Applejack', 'rarity': 'Rarity',
                 'pinkie': 'Pinkie Pie', 'rainbow': 'Rainbow Dash', 'fluttershy': 'Fluttershy'}
    for name, full_name in pony_name.items():
        pony_name_sub = copy.deepcopy(pony_name)
        del pony_name_sub[name]
        for name_sub, full_name_sub in pony_name_sub.items():
            if full_name_sub.split()[0] != full_name_sub.split()[-1]:
                pony_name_sub[name_sub] = dt[dt.pony == full_name].dialog.str.count('(?<!\w)' + str.split(full_name_sub)[0] + '(?!\w)').sum(axis=0) + \
                                          dt[dt.pony == full_name].dialog.str.count('(?<!\w)' + str.split(full_name_sub)[-1] + '(?!\w)').sum(axis=0) - \
                                          dt[dt.pony == full_name].dialog.str.count('(?<!\w)' + full_name_sub + '(?!\w)').sum(axis=0)
            else:
                pony_name_sub[name_sub] = dt[dt.pony == full_name].dialog.str.count(
                    '(?<!\w)' + full_name_sub + '(?!\w)').sum(axis=0)
        total_count = sum(pony_name_sub.values())
        for name_sub, full_name_sub in pony_name_sub.items():
            if pony_name_sub[name_sub] != 0:
                pony_name_sub[name_sub] = round(pony_name_sub[name_sub]/total_count, 2)
            else:
                pony_name_sub[name_sub] = 0
        ment[name] = pony_name_sub

def getFoll(dt,foll):
    # follow_on_comments
    pony_name = {'twilight': 'Twilight Sparkle', 'applejack': 'Applejack', 'rarity': 'Rarity', 'pinkie': 'Pinkie Pie',
                 'rainbow': 'Rainbow Dash', 'fluttershy': 'Fluttershy', 'other': 'non_Pony'}

    pony_list = list(dt['pony'])
    pony_list = list(map(is_non_pony, pony_list))
    pony_list = np.asarray(pony_list)

    for name, full_name in pony_name.items():
        if name == 'other':
            continue
        pony_name_sub = copy.deepcopy(pony_name)
        del pony_name_sub[name]
        index = np.nonzero(pony_list == full_name)[0] - 1
        for name_sub, full_name_sub in pony_name_sub.items():
            pony_name_sub[name_sub] = sum(pony_list[index] == full_name_sub)
        total_count = sum(pony_name_sub.values())
        for name_sub, full_name_sub in pony_name_sub.items():
            pony_name_sub[name_sub] = round(pony_name_sub[name_sub] / total_count, 2)
        foll[name] = pony_name_sub

def getNon_dict(dt,non_dict,dictionary_for_checking):
    # non_dictionary_words
    dict_words = dictionary_for_checking
    pony_name = {'twilight': 'Twilight Sparkle', 'applejack': 'Applejack', 'rarity': 'Rarity', 'pinkie': 'Pinkie Pie',
                 'rainbow': 'Rainbow Dash',
                 'fluttershy': 'Fluttershy'}
    pony_list = list(dt['pony'])
    pony_list = list(map(is_non_pony, pony_list))
    pony_list = np.asarray(pony_list)
    dia_list = list(dt['dialog'])
    dia_list = np.asarray(dia_list)

    for x,y in pony_name.items():
        non_dict[x] = Counter()

    for name, full_name in pony_name.items():
        dia = ' '.join(dia_list[pony_list == full_name])
        dia = words_cleanning(dia)
        dia = UnicodeToSpace(dia)
        for word in dia.split():
            if word.lower() not in dict_words:
                non_dict[name][word.lower()] += 1
        non_dict[name] = non_dict[name].most_common(5)
        non_dict[name] = [i[0] for i in non_dict[name]]