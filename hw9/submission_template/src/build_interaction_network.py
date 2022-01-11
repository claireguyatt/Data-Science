import argparse
import pandas as pd
import numpy as np
import networkx as nx
import json

# return csv char data in list of lists containing chars only by episode
def prepare_data(file_name):

    # put input csv into df
    df = pd.read_csv(file_name, header=0)

    # make all lowercase
    for columns in df.columns:
        df[columns] = df[columns].str.lower()

    # split up into dict by episode 
    titles = df['title'].unique()
    episodes = []
    for title in titles:
        
        temp = df[df['title'] == title]
        episodes.append(temp)

    # input only character column for each episode into list
    chars_by_episode = []
    for episode in episodes:
        temp = episode.pony.to_list()
        chars_by_episode.append(temp)

    # return list of lists of ponies
    return chars_by_episode

# get 101 most common chars (excluding all/ ands/ etc.)
def get_chars(lists):

    # merge all the characters into one list again
    all = []
    for episode in lists:
        all = all + episode

    # put list into df and get rid of invalid characters
    header = ["pony"]
    df = pd.DataFrame(all, columns=header)
    df = df[~df['pony'].str.contains('all|ponies|and|others')]

    # return list of the 101 most common 
    mains = df['pony'].value_counts()[:101].index.tolist()
    return mains

def get_network_data(lists, mains):

    # change invalid characters from every episode to None
    not_valids = ["All", "Ponies", " and ", "Others", "ponies"]
    for episode in lists:
        for i in range(len(episode)):
            for discard in not_valids:
                if discard in episode[i]:
                    episode[i] = None
                    break

    # make corresponding list for interactions and add each to a total df
    dfs = []
    for episode in lists:
        interactions = []
        for i in range(len(episode)-1):
            interactions.append(episode[i+1])
        # make last character interaction None
        interactions.append(None)
        # make data frame out of the 2 lists
        char_intrs = pd.DataFrame(list(zip(episode, interactions)),
               columns =['character', 'interaction'])
        dfs.append(char_intrs)
    
    # merge all dfs
    network = pd.concat(dfs)

    # delete rows with None or with matching char and interaction (aka talking to themself)
    network = network.dropna()
    network = network[~(network['character']==network['interaction'])]

    # delete rows with any characters that aren't in the top 100
    network = network[network['character'].isin(mains)]
    network = network[network['interaction'].isin(mains)]

    # reset df index & return
    pd.DataFrame.reset_index(network, inplace=True)
    return network

def create_network(network_df, mains, output):
    
    network = {}
    # make interaction list for each of the top ponies
    for main in mains:
        # make interactions of the main pony with each of the other ponies
        intrs_count = {}
        for intr in mains:
            temp = network_df[network_df['character']==main]
            temp = temp[network_df['interaction']==intr]
            temp2 = network_df[network_df['character']==intr]
            temp2 = temp2[network_df['interaction']==main]
            matches = len(temp) + len(temp2)
            if matches != 0:
                intrs_count[intr] = matches
        network[main] =  intrs_count

    # return json file containing the network
    with open(output, 'w') as f:
        json.dump(network, f, indent=4)

def main():

    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help = "input filename")
    parser.add_argument("-o", help = "output filename")
    args = parser.parse_args()
    input = args.i
    output = args.o

    # get just the ordered list of characters
    data = prepare_data(input)

    # from the list of lists, get a list of the 101 most common (& valid)
    mains = get_chars(data)
    
    # put all the chars and their valid interactions into a df
    network_df = get_network_data(data, mains)

    # create the json network
    create_network(network_df, mains, output)

if __name__ == '__main__':
    main()