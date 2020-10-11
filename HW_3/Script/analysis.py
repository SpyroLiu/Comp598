# This is a sample Python script.

import os
import argparse
import os.path as osp
import sys
from hw3.json_pony import create_json_pony

dire = osp.dirname(__file__)
dict_words_path = osp.join(dire, "..", "data", "words_alpha.txt")
# dict_words_path = '/Users/tylerliu/GitHub/Comp598/HW_3/data/words_alpha.txt'

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', help='The path to the .csv file')
    parser.add_argument('-o', metavar='File_Name', default=sys.stdout, help='File name. If given, the JSON output is written to that file. If not, it is written to stdout')
    # args = parser.parse_args(['/Users/tylerliu/GitHub/Comp598/HW_3/data/clean_dialog.csv', '-o abc'])
    args = parser.parse_args()
    src_file = args.csv_path
    save_file = args.o

    dict_words = open(dict_words_path)
    dict_words = set(dict_words.read().split('\n'))
    analysis_result = create_json_pony(src_file, dict_words)

    if isinstance(save_file, str):
        with open(save_file,'w') as f:
            f.write(analysis_result)
    else:
        sys.stdout.write(analysis_result)

    # print('Hello World')