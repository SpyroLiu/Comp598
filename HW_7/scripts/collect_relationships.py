import os.path as osp
import argparse
import json
import re
import sys
import requests
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


def filter_dating_people(candidate_links, person_url):
    relationships = []
    for link in candidate_links:
        if 'href' not in link.attrs:
            continue
        href = link['href']
        if href.startswith('/dating') and href != person_url:
            relationships.append(href)
    return relationships


def get_relationship(content,person_url):
    soup = BeautifulSoup(content,'html.parser')
    status_h4 = soup.find('h4', 'ff-auto-status')

    if not status_h4:
        return []
    key_div = status_h4.next_sibling
    candidate_links = key_div.find_all('a')
    relationships = []
    relationships.extend(filter_dating_people(candidate_links, person_url))

    if len(relationships) > 1:
        raise Exception('Too many current relationships! It should be 1')
    rels_h4 = soup.find('h4', 'ff-auto-relationships')
    if rels_h4 is not None:
        sib = rels_h4.next_sibling
        while sib is not None and sib.name == 'p':
            candidate_links = sib.find_all('a')
            sib = sib.next_sibling
            relationships.extend(filter_dating_people(candidate_links, person_url))

    # Remove some weird cases
    relationships = list(set(relationships))
    return  relationships

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help = 'The config file path')
    parser.add_argument('-o', help = 'The output file path')
    args = parser.parse_args()
    if not args.c or not args.o:
        print("Incomplete input")
        sys.exit()
    config_path = args.c
    output_path = args.o
    with open(config_path,'r') as json_file:
        config = json.load(json_file)
    tr = config['target_people']
    cache_path = config['cache_dir']

    relationship_dict = {}
    for p in tr:
        url = "https://www.whosdatedwho.com/dating/" + p
        content = get_url_contents(cache_path,url)
        rel = get_relationship(content, f'/dating/{p}')
        relationship_dict[p] = rel
    for k in relationship_dict.keys():
        new_v = []
        for element in relationship_dict[k]:
            new_v = new_v + [element.split('/')[-1]]
        print(new_v)
        relationship_dict[k] = new_v
    with open(output_path, 'w', encoding='utf-8') as fh:
        json.dump(relationship_dict,fh)
if __name__ == '__main__':
    main()
