import pandas as pd
import json
import random
import argparse
import sys

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="The output path")
    parser.add_argument("json_file", help=' The json file path')
    parser.add_argument("num_of_posts", help='How many posts to output')
    args = parser.parse_args()
    if not args.o or not args.json_file or not args.num_of_posts:
        print('Incomplete input')
        sys.exit()

    output_path = args.o
    json_path = args.json_file
    num = int(args.num_of_posts)

    posts = get_post_list(json_path)
    # Take samples from a list randomly without replacement
    sample_posts = random.sample(posts, min(num,len(posts)))
    df = pd.DataFrame(columns=['Name', 'title', 'coding'])
    for i in range(len(sample_posts)):
        p = posts[i]['data']
        name = p['name']
        title = p['title']
        coding = ''
        df = df.append({'Name': name, 'title': title, 'coding': coding}, ignore_index=True)

    df.to_csv(output_path, sep="\t", index=False)

if __name__ == '__main__':
    main()