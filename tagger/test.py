from tagger import *
from os import path
import unittest


class tagger_test(unittest.TestCase):

    def testOne(self):
        

        #CHANGE BLOG DIRECTORY
        blog_directory = 'entries-output'
        dict1 = 'anew.txt'
        d = [dict1]
        t = Tagger(d)
        t.tag_directory(blog_directory)
        t.get_tagged_from_high_coverage(50)
        t.get_high_coverage_blogs(50)
        # t.get_dense_scored_tagged(500)

        l = get_list_of_ids('id_coverage.txt')
        get_blogs_from_ids('top_coverage_entries.txt', l, 'entries')

        # l = get_list_of_ids('training_absolute.txt')
        # get_blogs_from_ids('top_absolute_entries.txt', l, 'entries')


if __name__ == '__main__':
    unittest.main()
