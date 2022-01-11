import os, sys
import argparse
import hashlib
import requests
import json
from bs4 import BeautifulSoup

# cache page
def cache_relations(URL, dir):

    # check if in cache
    hash = hashlib.sha1(URL.encode("UTF-8")).hexdigest()
    path = dir + "/" + hash
    full_cache_file_path = (os.path.abspath(os.getcwd()) + "/" + path)
    if (os.path.isfile(full_cache_file_path)==False):
        # if not get it and add it to cache dir
        req = requests.get(URL)
        page = req.text
        with open(path, 'w') as fh:
            fh.write(str(page))
    # return path to file in the cache dir either way
    return path

# fetch relationships
def fetch_relations(page, name):
    
    # open file with beautifulsoup to start scraping
    soup = BeautifulSoup(open(page, 'r'), 'html.parser')

    # list to add relations to
    relations = list()

    # find div that contains paragraphs that list relations
    block = soup.find('div', class_='ff-block-content dating-profile')

    # need all types:
    types = ['was previously married to', 'has been in relationships with', 'has had encounters with', 
                'is rumoured to have hooked up with', 'has been engaged to']

    # if currently in relationship
    try:
        current = soup.find('div', style='position:relative;width:51%;padding-left:108px;height:130px;margin-bottom:20px;')
        a = current.find('a')
        # make sure it's returning the relation not the person themselves
        # (depends on how the sentence was written)
        first_name = a.string.split()[0].lower()
        # if it's the target, get their relation instead
        if first_name in name:
            a = current.find_all('a')
            relations.append(a[1].string)
        else:
            relations.append(a.string)
    except:
        pass

    # find paragraphs within div
    paragraphs = block.find_all('p')
    for p in paragraphs:
        # only get the relations paragraphs
        for t in types:
            if t in p.text:
                # get anchors from relation paragraph
                anchors = p.find_all('a')
                for a in anchors:
                    relations.append(a.string)
    return relations

def main():
    
    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help = "config filename")
    parser.add_argument("-o", help = "output filename")
    args = parser.parse_args()
    input = args.c
    output = args.o

    # get info from config file
    with open(input, 'r') as f:
        config = json.load(f)
    cache_dir = config['cache_dir']
    # make cache dir if not already there
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    targets = config['target_people']

    # make new list of targets but with URLs instead of people
    urls = []
    for name in targets:
        url = "https://www.whosdatedwho.com/dating/" + name
        urls.append(url)

    # make paired list of names & urls
    pairs = zip(targets, urls)

    final = {}
    # do the thing
    for name, url in pairs:
        # first make sure its in cache dir
        path_to_cachef = cache_relations(url, cache_dir)
        # fetch the info from the cache file
        relations = fetch_relations(path_to_cachef, name)
        # output json of relations
        final[name] = relations
    
    # make json to return
    with open(output, "w") as out_file:
        json.dump(final, out_file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()