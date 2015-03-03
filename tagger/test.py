from tagger import *
from os import path
import unittest


class tagger_test(unittest.TestCase):

    def testOne(self):
        blog_directory = 'entries-output'
        
        # top_words = extract_top_words(blog_directory)
        # l = map_unigrams('entries-output/2143.txt.xml', top_words)
        # format_to_libsvm(l)
        

        #CHANGE BLOG DIRECTORY
        dict1 = 'anew.txt'
        dict2 = 'nrc.txt'
        d = dict1
        t = Tagger(d, 'anew')
        
        t.tag_directory(blog_directory)

        t.score_valence()
        l = get_list_of_ids('id_scored_valence.txt')
        get_blogs_from_ids('top_scored_valence.txt', l, 'entries')


        # t.score_joy()
        # l = get_list_of_ids('id_scored_joy.txt')
        # get_blogs_from_ids('top_scored_joy.txt', l, 'entries')


        # t.get_tagged_from_high_coverage(50)
        # t.get_high_coverage_blogs(50)
        # t.get_high_occurrence_blogs(50)

if __name__ == '__main__':
    unittest.main()
