import sys
import json

def av_title_length(file):

    count = 0
    with open(file, 'r') as f:
        for line in f:
            # load each line of the json
            l = f.readline()
            post = json.loads(l)
            # access the title
            title = post['data']['title']
            # add title length to total count
            length = len(post['data']['title'])
            count = count + length
    # divide total length by 1000 (posts)
    count = count/1000
    # print av length
    print(file + " average title length:", count)

def main():
    input_file = sys.argv[1]
    av_title_length(input_file)

if __name__ == '__main__':
    main()