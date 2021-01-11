import os.path as osp
import argparse
import re
import sys
import requests
import json
from bs4 import BeautifulSoup
import hashlib
dir_file = osp.dirname(__file__)

def get_url_contents(cache_path,url):
    fname = hashlib.sha1(url.encode('utf-8')).hexdigest()
    full_name = osp.join(cache_path,fname)
    content = None
    if osp.exists(full_name):
        # print("Loading from cache")
        content = open(full_name,'r').read()
    else:
        # print("Loading from source")
        r = requests.get(url)
        content = r.text
        with open(full_name,'w') as fh:
            fh.write(content)
    return content

def get_course_info(content):
    soup = BeautifulSoup(content,'html.parser')
    status_h4 = soup.find_all('h4',"field-content")
    ls = []
    for line in status_h4:
        line = str(line)
        if bool(re.search(">(?=[A-Z])[\w\d\s]* \(.* credit[s]?\)<",line)):
            p = re.compile(">(?=[A-Z])[\w\d\s]* \(.* credit[s]?\)<")
            result = p.search(line)
            if result:
                course_info = result.group(0)
                ls.append(course_info[1:-1])
    return ls

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help = 'The cache directory')
    parser.add_argument('page', help = 'The number of page from which the data is extracted')
    args = parser.parse_args()
    if not args.c or not args.page:
        print("Incomplete input")
        sys.exit()
    args.page ='https://www.mcgill.ca/study/2020-2021/courses/search?page='+str(args.page)
    content = get_url_contents(args.c,args.page)
    tmp = get_course_info(content)
    print("CourseID, Course Name, # of credits")
    for i in tmp:
        i = i.split(' ')
        course_id = ' '.join(i[0:2])
        course_name = ' '.join(i[2:-2])
        course_credit = i[-2][1:]
        print(f'{course_id},{course_name},{course_credit}')

if __name__ == '__main__':
    main()