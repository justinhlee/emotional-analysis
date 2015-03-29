from tagger import *
from formatter import *
from os import path
import unittest


class tagger_test(unittest.TestCase):

    # def testTesting(self):
    #     top_words_directory = 'midsize-output'
    #     testing_directory = 'testing-output'
    #     dict1 = 'nrc.txt'
    #     create_testing_set_nrc(top_words_directory, testing_directory, dict1)

    def testTraining(self):
        blog_directory = 'midsize-output'
        dict1 = 'nrc.txt'
        create_training_set_nrc(blog_directory, dict1)

    # def testTrainingSet(self):
    #     blog_directory = 'midsize-output'
    #     top_words = extract_top_words(blog_directory)
    #     print 'Number of features: ' + str(len(top_words))
    #     dict1 = 'anew.txt'
    #     d = dict1
    #     t = Tagger(d, 'anew')
    #     t.tag_directory(blog_directory)
    #     towrite = open('training', 'w')

    #     t.score_valence(True)
    #     ids = get_list_of_ids('id_scored_valence.txt')
    #     os.remove('id_scored_valence.txt')

    #     n = len(ids)
    #     completed = 0

    #     for blog_id in ids:
    #         path = 'midsize-output/' + blog_id + '.xml'
    #         towrite.write(format_to_libsvm(map_unigrams(path, top_words), True) + '\n')
    #         completed += 1
    #         if (completed % 100) == 0:
    #             print '%.2f' % (completed*100/float(n)) + '% of training data written.'

    #     t.score_valence(False)
    #     ids = get_list_of_ids('id_scored_valence.txt')

    #     n = n + len(ids)
    #     for blog_id in ids:
    #         path = 'midsize-output/' + blog_id + '.xml'
    #         towrite.write(format_to_libsvm(map_unigrams(path, top_words), False) + '\n')
    #         completed += 1
    #         if (completed % 100) == 0:
    #             print '%.2f' % (completed*100/float(n)) + '% of training data written.'
    #     towrite.close()

    # def testTrainingSetNRC(self):
    #     blog_directory = 'midsize-output'
    #     top_words = extract_top_words(blog_directory)
    #     print 'Number of features: ' + str(len(top_words))
    #     dict1 = 'nrc.txt'
    #     d = dict1
    #     t = Tagger(d, 'nrc')
    #     t.tag_directory(blog_directory)
    #     towrite = open('training', 'w')

    #     t.score_joy(True)
    #     ids = get_list_of_ids('id_scored_joy.txt')
    #     os.remove('id_scored_joy.txt')

    #     n = len(ids)
    #     completed = 0

    #     for blog_id in ids:
    #         path = blog_directory + '/' + blog_id + '.xml'
    #         towrite.write(format_to_libsvm(map_unigrams(path, top_words), True) + '\n')
    #         completed += 1
    #         if (completed % 100) == 0:
    #             print '%.2f' % (completed*100/float(n)) + '% of training data written.'

    #     t.score_joy(False)
    #     ids = get_list_of_ids('id_scored_joy.txt')

    #     n = n + len(ids)
    #     for blog_id in ids:
    #         path = blog_directory + '/' + blog_id + '.xml'
    #         towrite.write(format_to_libsvm(map_unigrams(path, top_words), False) + '\n')
    #         completed += 1
    #         if (completed % 100) == 0:
    #             print '%.2f' % (completed*100/float(n)) + '% of training data written.'
    #     towrite.close()

    # def testOne(self):
    #     pass

        # PSEUDOCODE FOR PROCESSING
        # 1. extract_top_words
        # 2. tag_directory
        # 3. score_label
        # 4. get_blog_ids
        # 5. for each id: map_unigram and format_to_libsvm


        # blog_directory = 'entries-output'
        # blog_directory = 'testing-output'
        # top_words = extract_top_words(blog_directory)
        # print map_unigrams('entries-output/1.txt.xml', top_words)
        #extract_similarity(top_words)

        # blog_directory = 'testing-output'
        # dict1 = 'anew.txt'
        # d = dict1
        # t = Tagger(d, 'anew')
        # t.tag_directory(blog_directory)
        # towrite = open('testing.t', 'w')
        
        # t.get_high_coverage_blogs(150)
        # ids = get_list_of_ids('id_coverage.txt')
        # get_blogs_from_ids('testing-entries.txt', ids, 'testing-entries')
        # n = len(ids)
        # completed = 0
        # for blog_id in ids:
        #     path = 'testing-output/' + blog_id + '.xml'
        #     towrite.write(format_to_libsvm(map_unigrams(path, top_words), True) + '\n')
        #     completed += 1
        #     if (completed % 30) == 0:
        #         print '%.2f' % (completed*100/float(n)) + '% of testing data written.'



        # dict2 = 'nrc.txt'
      
        # dict1 = 'anew.txt'
        # d = dict1
        # t = Tagger(d, 'anew')
        # t.tag_directory(blog_directory)
        # towrite = open('training', 'w')

        # t.score_valence(True)
        # ids = get_list_of_ids('id_scored_valence.txt')
        # os.remove('id_scored_valence.txt')

        # n = len(ids)
        # completed = 0

        # for blog_id in ids:
        #     path = 'entries-output/' + blog_id + '.xml'
        #     towrite.write(format_to_libsvm(map_unigrams(path, top_words), True) + '\n')
        #     completed += 1
        #     if (completed % 30) == 0:
        #         print '%.2f' % (completed*100/float(n)) + '% of training data written.'

        # t.score_valence(False)
        # ids = get_list_of_ids('id_scored_valence.txt')

       


        # n = n + len(ids)
        # for blog_id in ids:
        #     path = 'entries-output/' + blog_id + '.xml'
        #     towrite.write(format_to_libsvm(map_unigrams(path, top_words), False) + '\n')
        #     completed += 1
        #     if (completed % 30) == 0:
        #         print '%.2f' % (completed*100/float(n)) + '% of training data written.'
        # towrite.close()


      

if __name__ == '__main__':
    unittest.main()
