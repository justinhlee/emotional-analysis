from tagger import *
import unittest


class tagger_test(unittest.TestCase):

    def testOne(self):
        dict1 = 'anew.txt'
        d = [dict1]
        t = Tagger(d)
        t.tag_directory('samples')
        t.get_high_scored_blogs(10)
        t.get_dense_scored_blogs(10)
        b = t.get_blog_by_id('764')
        print b

if __name__ == '__main__':
    unittest.main()
