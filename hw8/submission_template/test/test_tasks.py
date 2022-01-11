import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.compile_word_counts import *
from src.compute_pony_lang import *

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        self.ponies = ponies = ['twilight sparkle','applejack','rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']

    def test_task1(self):

        print(f"Test compile_word_counts:")
        print("Note: Regex warning will print in running this test. This does not mean anything went wrong.\n")

        # dict to send to final function
        dicts = {}

        # send test csv through the functions in compile_word_counts.py
        lows = get_lows(self.mock_dialog, self.ponies)
        for pony in self.ponies:
            pony_dict = pony_words(self.mock_dialog, lows, pony)
            dicts[pony] = pony_dict
        result = return_json('tester_output.json', dicts)

        # open real file to compare
        with open(self.true_word_counts, 'r') as f:
            real = json.load(f)

        # compare resultant dict to real dict (jsons)           
        if self.assertDictEqual(result, real):
            print("OK")

        # delete tester file
        os.remove('tester_output.json')

    def test_task2(self):

        print(f"Test compute_pony_lang:")

        # dict to send to final function
        counts = {}

        # open up real word count file to use to test tfidf
        with open(self.true_word_counts, 'r') as f:
            real_word_counts = json.load(f)
        
        # send word count file to compute_pony_lang & run through functions
        test_idfs = compute_idf(real_word_counts)

        for pony in self.ponies:
            test_tfidfs = compute_tfidf(pony, test_idfs, 100)
            counts[pony] = test_tfidfs
        
        # load result dict into json to test
        with open('test.json', 'w') as f:
            json.dump(counts, f, indent=4)
        with open('test.json', 'r') as f:
            result = json.load(f)
        
        # load real tf idf json dict to test against
        with open(self.true_tf_idfs, 'r') as f:
            real = json.load(f)

        # compare result to real
        if self.assertDictEqual(result, real):
            print("OK")

        # delete test files created
        os.remove('test.json')
    
if __name__ == '__main__':
    unittest.main()