# compute word counts for each word for ponies in mlp

import os
import pandas as pd
import argparse
import json

# edit df (punctuation, alphabetic) & get freq count list
def get_freqs(dataset):

    # get rid of punctuation
    punctuation = '()[],-.?!:;#&' 
    for char in punctuation:
        dataset['dialog'] = dataset['dialog'].str.replace(char, ' ')
   
    # list of words with total freq counts
    word_freq = pd.DataFrame(dataset.dialog.str.split(expand=True).stack().value_counts())
    word_freq.reset_index(level=0, inplace=True)
    word_freq.columns = ['word', 'freq']

    # get rid of words that aren't alphabetic
    # make column that is True for alphabetic words
    word_freq['is_alpha'] = list(map(lambda x: x.isalpha(), word_freq['word']))
    # delete nonalpha words based on alpha column truth value
    word_freq.drop(word_freq.index[word_freq['is_alpha'] == False], inplace=True)

    return word_freq

# get list of low freq words
def get_lows(input, ponies):
    
    # put csv into pandas df
    dataset = pd.read_csv(input)

    # make all lowercase
    for columns in dataset.columns:
        dataset[columns] = dataset[columns].str.lower()

    # get only valid pony speech acts
    dataset = dataset.loc[dataset['pony'].isin(ponies)]

    word_freq = get_freqs(dataset)
    
    # get list of words with < 5 occurrences (too low freq)
    lows = word_freq[word_freq['freq'] < 5]

    # return just the low freq word list 
    lows = lows['word'].tolist()
    return lows

def pony_words(input, lows, pony):

    # put csv into pandas df & then get just the input pony
    dataset = pd.read_csv(input)

    # make all lowercase (for name purposes)
    for columns in dataset.columns:
        dataset[columns] = dataset[columns].str.lower()
        
    # change dataset to only input pony
    dataset = dataset[dataset['pony'] == pony]

    word_freq = get_freqs(dataset)

    # get rid of words with low freq
    for word in lows:
        word_freq = word_freq[word_freq['word'] != word]
    
    # get rid of stop words (too  high freq)
    with open('data/stopwords.txt', 'r') as stop_file:
    
        stops = stop_file.readlines()
        # delete stop words
        for word in stops:
            clean_word = word.strip('\n')
            word_freq = word_freq[word_freq['word'] != clean_word]
    
    # return just dict of words with their freq counts
    freq_dict = word_freq.set_index('word').to_dict()['freq']
    return freq_dict

def return_json(output, final_dict):
    
    # for the output file, you should create directories if they do not exist.

    dir = os.path.dirname(output)
    exists = os.path.isdir(dir)

    if exists == False:
        os.makedirs(dir)

    with open(output, 'w') as f:
        json.dump(final_dict, f, indent=4)
    
    # for test purposes
    with open(output, 'r') as f:
        test_file = json.load(f)
    
    return test_file

def main():

    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help = "input filename")
    parser.add_argument("-o", help = "output filename")
    args = parser.parse_args()
    input = args.d
    output = args.o

    # list of ponies of interest
    ponies = ['twilight sparkle','applejack','rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']

    # get low freq word list
    lows = get_lows(input, ponies)

    # empty list to add pont word count dicts to
    counts = {}

    # get word counts for each pony & add to list
    for pony in ponies:
        
        pony_dict = pony_words(input, lows, pony)
        counts[pony] = pony_dict

    # make final output json
    return_json(output, counts)

if __name__ == '__main__':
    main()