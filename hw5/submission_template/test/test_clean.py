import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.clean import *

class CleanTest(unittest.TestCase):
    def setUp(self):

        self.clean_file_path = os.path.join(parentdir, 'src')

        # fixture1: wrong title
        self.open1 = open("test/fixtures/test_1.json", "r")
        # fixture 2: wrong createdAt
        self.open2 = open("test/fixtures/test_2.json", "r")
        # fixture 3: wrong json file
        self.open3 = open("test/fixtures/test_3.json", "r")
        # fixture 4: wrong author
        self.open4 = open("test/fixtures/test_4.json", "r")
        # fixture 5: uncastable string for count
        self.open5 = open("test/fixtures/test_5.json", "r")
        # fixture 6: 3 words in 1 tag
        self.open6 = open("test/fixtures/test_6.json", "r")

        print("\nRUNNING TESTS FOR HW5 - clean.py")

    def test_title_check(self):

        line1 = self.open1.readline()
        post1 = json.loads(line1)
        print("json without title")
        self.assertIsNone(title_check(post1))

    def test_time_check(self):

        line2 = self.open2.readline()
        post2 = json.loads(line2)
        print("json with invalid createdAt")
        self.assertIsNone(time_check(post2))

    def test_get_valid(self):

        line3 = self.open3.readline()
        print ("invalid json")
        self.assertIsNone(get_valid(line3))

    def test_author_check(self):

        line4 = self.open4.readline()
        post4 = json.loads(line4)
        print("json with invalid author")
        self.assertIsNone(author_check(post4))
    
    def test_count_check(self):
        
        line5 = self.open5.readline()
        post5 = json.loads(line5)
        print("json with uncastable string count")
        self.assertIsNone(count_check(post5))

    def test_tags_check(self):

        line6 = self.open6.readline()
        post6 = json.loads(line6)
        print("json with 3 words in 1 tag")
        # check that post gets returned
        self.assertEqual(tags_check(post6), post6)
        # check that words were split
        tags = "tags"
        for tag in post6[tags]:
            bool = True
            if (' ' in tag):
                bool = False
            self.assertTrue(bool)

    def tearDown(self):

        # close all opened file fixtures
        self.open1.close()  
        self.open2.close()
        self.open3.close()
        self.open4.close()
        self.open5.close()
        self.open6.close()

if __name__ == '__main__':
    unittest.main()