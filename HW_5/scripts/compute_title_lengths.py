import os.path as osp
import sys
script_dir = osp.dirname(__file__)
sys.path.insert(1, osp.join(script_dir, '..', 'src', 'hw5'))
import argparse
from subr_avg_title_length import get_subr_avg_title_length
from load_clean import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='The input json file path')
    args = parser.parse_args()
    if not args.file_path:
        print('No json file path received')
    else:
        input_path = args.file_path
        l = get_post_list(input_path)
        l = title_check(l)
        title_length = get_subr_avg_title_length(l)
        title_length = round(title_length, 2)
        print(title_length)


# p1 = osp.join(script_dir, '..', 'data', 'cleaned_sample1.json')
# c1 = get_post_list(p1)
# c1_avg = get_subr_avg_title_length(c1)
# print(c1_avg)