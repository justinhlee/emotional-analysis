from analyzer import *
from reader import *
import unittest


class analyzer_test(unittest.TestCase):

    # def testTesting(self):
    #     a = Analyzer('testing_w_id')
    #     a.count_multi_labels('../Testing')
    #     a.percent_multi_labels()

     def testReaderTesting(self):
        r = Reader('tagger_labels')
        r.count_multi_labels()


if __name__ == '__main__':
    unittest.main()
