import argparse
import json
import os.path as osp
import sys
script_dir = osp.dirname(__file__)
sys.path.insert(1, osp.join(script_dir, '..', 'src', 'hw5'))
import load_clean

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='The input file path')
    parser.add_argument('-o', help='The output file path')
    args = parser.parse_args()
    if not args.o or not args.i:
        print("Incomplete input!")
    else:
        input_path = args.i
        output_path = args.o
        fi = load_clean.get_post_list(input_path)
        fi = load_clean.title_check(fi)
        fi = load_clean.time_standardize(fi)
        with open(output_path, 'w', encoding='utf-8') as f:
            for p in fi:
                f.write(json.dumps(p))
                f.write('\n')

