import datetime
import pandas as pd
import numpy as np
import os.path as osp
import json

from random import sample

def getDuration(date1, date2):
    day = date1
    day = [day[0].split('/')[2],day[0].split('/')[0],day[0].split('/')[1],
           day[1].split(':')[0],day[1].split(':')[1],day[1].split(':')[2]]
    day = [int(i) for i in day]
    if date1[2] == 'PM':
        day[3] = day[3] + 12 * (day[3] != 12)
    else:
        day[3] = day[3] - 12 * (day[3] == 12)
    time1 = datetime.datetime(day[0], day[1], day[2], day[3], day[4], day[5], 0)

    day = date2
    day = [day[0].split('/')[2], day[0].split('/')[0], day[0].split('/')[1],
           day[1].split(':')[0], day[1].split(':')[1], day[1].split(':')[2]]
    day = [int(i) for i in day]
    if date2[2] == 'PM':
        day[3] = day[3] + 12 * (day[3] != 12)
    else:
        day[3] = day[3] - 12 * (day[3] == 12)
    time2 = datetime.datetime(day[0], day[1], day[2], day[3], day[4], day[5], 0)
    return (time2-time1).seconds/3600 + (time2-time1).days*24

def getMonth(date):
    return int(date.split('/')[0])

def getZipJson():
    script_dir = osp.dirname(__file__)
    csv_path = osp.join(script_dir,'..','data','new_nyc.csv')
    df = pd.read_csv(csv_path, header=None, usecols=[1, 2, 8])
    df = df[df[1].str.contains('2020')]
    df.dropna(inplace=True)
    df[8] = df[8].astype('int32')

    ls1 = list(map(str.split, df[1].astype('str')))
    ls2 = list(map(str.split, df[2].astype('str')))
    duration = np.asarray(list(map(getDuration, ls1, ls2)))
    index = duration >= 0
    duration = duration[index]

    close_month = df[2].apply(getMonth)
    close_month = close_month[index]
    case_zipcode = df[8][index]
    zipcode_list = set(case_zipcode)

    m_avg = [0] * 12

    for i in range(1, 13):
        k = sum(close_month == i)
        if k != 0:
            m_avg[i - 1] = sum(duration[close_month == i]) / k
        else:
            # m_avg[i - 1] = np.nan
            m_avg[i - 1] = 0

    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_avg_json = {}
    for i in range(0, 12):
        month_avg_json[month[i]] = m_avg[i]

    month_avg_json = json.dumps(month_avg_json, indent=2)
    path = osp.join(script_dir, '..', 'data', 'month_avg.json')
    with open(path,'w') as f:
        f.write(month_avg_json)

    zip_avg_json = {}
    for z in zipcode_list:
        zip_avg_json[z] = {}
        sub_index = case_zipcode == z
        s_case_zipcode = case_zipcode[sub_index]
        s_close_month = close_month[sub_index]
        s_duration = duration[sub_index]
        for i in range(1, 13):
            s_id = s_close_month == i
            k = sum(s_id)
            if k != 0:
                zip_avg_json[z][month[i - 1]] = sum(s_duration[s_id]) / k
            else:
                # zip_avg_json[z][month[i - 1]] = np.nan
                zip_avg_json[z][month[i - 1]] = 0
    zip_avg_json = json.dumps(zip_avg_json, indent=2)
    path = osp.join(script_dir, '..', 'data', 'zip_avg.json')
    with open(path,'w') as f:
        f.write(zip_avg_json)
