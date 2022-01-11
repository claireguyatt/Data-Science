import argparse
import pandas as pd
import numpy as np
import networkx as nx
import json

def networkx_setup(file_name):

    # open input file
    with open(file_name, 'r') as f:
        dict = json.load(f)
    
    # create network graph & add character by character
    char_nw = nx.Graph()

    characters = dict.keys()
    for char in characters:
        intr = dict[char].keys()
        for intr in dict[char]:
            char_nw.add_edge(char, intr, weight=dict[char][intr])

    return char_nw

def network_stats(char_nw):

    stats = {}

    # most connected characters by number of edges
    edges = list(char_nw.degree())
    characters_only = []
    for char in edges:
        characters_only.append(char[0])
    stats['most_connected_by_num'] = characters_only[:3]
    
    # most connected by sum of weight of edges
    weighted_edges = list(char_nw.degree(weight='weight'))
    characters_only = []
    for char in weighted_edges:
        characters_only.append(char[0])
    stats['most_connected_by_weight'] = characters_only[:3]

    # most central by betweenness
    betweenness = nx.betweenness_centrality(char_nw)
    characters_only = []
    for char in betweenness:
        characters_only.append(char)
    stats['most_central_by_betweenness'] = characters_only[:3]

    return stats

def main():

    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help = "input filename")
    parser.add_argument("-o", help = "output filename")
    args = parser.parse_args()
    input = args.i
    output = args.o

    # set up the network and use the info to get network stats
    char_network = networkx_setup(input)
    top3 = network_stats(char_network)

    # return stats in a json file
    with open(output, 'w') as f:
        json.dump(top3, f, indent=4)

if __name__ == '__main__':
    main()