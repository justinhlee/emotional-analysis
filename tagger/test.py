from tagger import *
from os import path
import unittest


class tagger_test(unittest.TestCase):

    def testOne(self):
        l = get_list_of_ids('training_normalized.txt')
        get_blogs_from_ids('top_normalized_entries.txt', l, 'entries')

        l = get_list_of_ids('training_absolute.txt')
        get_blogs_from_ids('top_absolute_entries.txt', l, 'entries')


        # blog_directory = 'samples'
        # dict1 = 'anew.txt'
        # d = [dict1]
        # t = Tagger(d)
        # t.tag_directory(blog_directory)
        # t.get_high_scored_blogs(500)
        # t.get_dense_scored_blogs(500)


if __name__ == '__main__':
    unittest.main()
