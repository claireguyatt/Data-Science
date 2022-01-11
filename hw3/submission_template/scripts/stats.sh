#!/bin/bash

File=$1

# print line count

echo "Number of lines in $File:" `cat $File | wc -l`

# print first line

echo "Header:" `head -n 1 $File`

# print # of lines in last 10,000 that have "potus"

tail -n 10000 $File | grep -c -i "potus"

head -n 200 $File | tail -100 | grep -wc "fake"
