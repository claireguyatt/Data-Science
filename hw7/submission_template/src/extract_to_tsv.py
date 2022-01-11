# accepts json file & outputs random selection of posts in a .tsv

import sys
import json
import random
import pandas as pd

# makes list of random posts from input json
def random_posts(infile, num_posts):

    # open file and write to list
    random_posts = {}
    with open(infile, 'r') as f:
        posts = json.load(f)
    
    # get num of posts specified (max 100)
    n = 0
    if num_posts >= len(posts):
        n = 100
    else:
        n = num_posts

    # randomly add posts and return list
    random_posts = (random.sample(posts, n))
    return random_posts


# make list of random posts in tsv format
def format_tsv(posts, outfile):

    # make new list with only the data dicts (don't need the 'kind' info)
    data = []
    for p in posts:
        data.append(p['data'])
    
    # make dataframe from post data & only keep required info
    df = pd.DataFrame(data)
    headers = ['name', 'title', 'coding']
    df = df.reindex(columns = headers)
    # capitalize 'name' header
    df.columns = ['Name' if x=='name' else x for x in df.columns]

    # turn into file in tsv format
    df.to_csv(outfile, sep = '\t', index=False)

def main():
    
    # use sys to assing input variables
    outfile = sys.argv[2]
    infile = sys.argv[3]
    num_posts = int(sys.argv[4])

    r_posts = random_posts(infile, num_posts)
    format_tsv(r_posts, outfile)

if __name__ == '__main__':
    main()