# compute word frequency in mlp

import argparse
import pandas as pd
import json
import math

# get total freq of all words
def compute_idf(pony_counts):

    # turn json into pd
    df = pd.DataFrame.from_dict(pony_counts)

    # get how many ponies used the word
    df['pony_use'] = df.count(axis=1)

    # get idf score for the word

    df['idf'] = 6/df['pony_use']
    # turn into list to log vals
    to_log = df['idf'].tolist()
    logged = [math.log10(i) for i in to_log]
    # put logged list back into df
    df['idf'] = logged

    # return pandas df containing idfs of all words
    return df

# get word freq list for a single pony
def compute_tfidf(pony, idfs, num_words):

    # keep target pony words
    pony_words = idfs[[pony, 'idf']]

    # get rid of NaN word rows
    pony_words = pony_words.dropna()

    # make tfidf column (multiply tf by idf)
    pony_words['tfidf'] = pony_words[pony]*pony_words['idf']

    # get input n highest words
    
    # sort by tfidf column
    pony_words = pony_words.sort_values(by=['tfidf'], ascending=False)
    # keep n rows
    pony_words = pony_words.head(num_words)

    # return word-tfidf pair dict
    word_tfidf = pony_words.set_index(pony_words.index).to_dict()['tfidf']
    return word_tfidf

def main():

    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help = "input filename of pony counts")
    parser.add_argument("-n", help = "output filename of tf-dif per pony")
    args = parser.parse_args()
    input = args.c
    num_words = int(args.n)

    # download input json
    with open(input, 'r') as f:
        pony_counts = json.load(f)

    # list of target ponies
    ponies = ['twilight sparkle','applejack','rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']

    # get idfs of all words
    idfs = compute_idf(pony_counts)

    # compute n highest freq words with tfidfs method
    counts = {}
    for pony in ponies:

        word_tfidf_pairs = compute_tfidf(pony, idfs, num_words)
        words_only = list(word_tfidf_pairs.keys())
        counts[pony] = words_only

    # print results in json form
    # *** need to print in one line at a time (right now separates by word)
    print(json.dumps(counts, indent=4))

if __name__ == '__main__':
    main()