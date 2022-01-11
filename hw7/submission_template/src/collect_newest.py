# script to collect 100 newest posts from the specified subreddit

import requests
import argparse
import json
import os

# authentication - download & save data from input URL
def get_data(subreddit):

    # personal app & account stuff
    ID = "QLww140vMx0fDn80hXTHmA"
    secret = "y3CB4q_9sz-n2NqSUQ3q5sGJqc-sMA"
    uname = "COMP598_DataAnal"
    pw = "LeoIsSexy123"

    # nrequest OAuth token
    auth = requests.auth.HTTPBasicAuth(ID, secret)

    # login method (username & pw)
    data = {'grant_type': 'password', 'username': uname, 'password': pw}

    # setup header info (give reddit a brief description of app)
    headers = {'User-Agent': 'DataAnalforClass/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) add headers=headers to requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    # get & return json using input subreddit
    string  = "https://oauth.reddit.com" + subreddit + "/new.json?limit=100"
    res = requests.get(string, headers=headers)
    return res.json()

# format and create jsons
def output(data, output_f):
    
    # get data from reddit API & put into json file
    with open('temp.json', 'w') as f:
        json.dump(data, f)
    with open('temp.json', 'r') as f:
        data = json.load(f)
    # change into dict and get rid of outter part (so just keep children)
    posts = data['data']['children']

    # get rid of temp file
    os.remove('temp.json')

    with open(output_f, 'w') as f:
        f.write('[' + ',\n'.join(json.dumps(p) for p in posts) + ']\n')

def main():
    
    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help = "output file")
    parser.add_argument("-s", help = "subreddit")
    args = parser.parse_args()
    output_f = args.o
    subreddit = args.s

    # create formatted jsons
    data = get_data(subreddit)
    output(data, output_f)

if __name__ == '__main__':
    main()