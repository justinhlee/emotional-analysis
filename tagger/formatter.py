import os
import operator
import math
from random import randint
from tagger import *


# def create_training_set_anew(blog_directory, dict_path):
#     top_words = read_top_words('top_words.txt')
#     t = Tagger(dict_path)
#     t.tag_directory(blog_directory)
    
emotions = ['anger', 'anticipation', 'disgust', 'fear'
            , 'joy', 'negative', 'positive', 'sadness'
            , 'surprise', 'trust']

def create_training_set_anew(blog_directory, dict_path):
    top_words = read_top_words('top_words.txt')
    t = Tagger(dict_path)
    t.tag_directory(blog_directory)
    for i in range(1):
        threshold = 7.0
        towrite = open('training' + str(i), 'w')
        t.score_valence(True, i, threshold, 2000)
        ids = get_list_of_ids('id_scored.txt')
        n = len(ids)
        completed = 0
        for blog_id in ids:
            path = blog_directory + '/' + blog_id + '.xml'
            towrite.write(format_to_libsvm(map_unigrams(path, top_words), True) + '\n')
            completed += 1
            if (completed % 100) == 0:
                print '%.2f' % (completed*100/float(n)) + '% of training data written.'
        t.score_valence(False, i, threshold, n)
        ids = get_list_of_ids('id_scored.txt')
        n = n + len(ids)
        print n
        for blog_id in ids:
            path = blog_directory + '/' + blog_id + '.xml'
            towrite.write(format_to_libsvm(map_unigrams(path, top_words), False) + '\n')
            completed += 1
            if (completed % 100) == 0:
                print '%.2f' % (completed*100/float(n)) + '% of training data written.'
        towrite.close()



def create_training_set_nrc(blog_directory, dict_path):
    # top_words = extract_top_words(blog_directory)
    top_words = read_top_words('top_words.txt')
    #top_words = extract_top_labels(dict_path)
    t = Tagger(dict_path)
    t.tag_directory(blog_directory)
    for i in range(10):
        towrite = open('training' + str(i), 'w')
        # threshold for nrc (consider putting it in as argument)
        threshold = 0.25
        t.score_nrc(True, i, threshold, 2000)
        ids = get_list_of_ids('id_scored.txt')
        os.remove('id_scored.txt')
        n = len(ids)
        completed = 0
        for blog_id in ids:
            path = blog_directory + '/' + blog_id + '.xml'
            towrite.write(format_to_libsvm(map_unigrams(path, top_words), True) + '\n')
            completed += 1
            if (completed % 100) == 0:
                print '%.2f' % (completed*100/float(n)) + '% of training data written.'
        t.score_nrc(False, i, threshold, n)
        ids = get_list_of_ids('id_scored.txt')
        n = n + len(ids)
        print n
        for blog_id in ids:
            path = blog_directory + '/' + blog_id + '.xml'
            towrite.write(format_to_libsvm(map_unigrams(path, top_words), False) + '\n')
            completed += 1
            if (completed % 100) == 0:
                print '%.2f' % (completed*100/float(n)) + '% of training data written.'
        towrite.close()


def create_testing_set_nrc(testing_directory, dict_path):
    #top_words = extract_top_words(top_words_directory)
    top_words = read_top_words('top_words.txt')
    t = Tagger(dict_path)
    t.tag_directory(testing_directory)
    towrite = open('testing.t', 'w')
    with_id = open('testing_w_id', 'w')
    ids = []
    # random entry id
    for i in range(200):
        r_int = randint(0, 4789)
        b_id = str(r_int) + '.txt'
        ids.append(b_id)
    get_blogs_from_ids('testing-entries.txt', ids, '../data/testing-entries')
    n = len(ids)
    completed = 0
    for blog_id in ids:
        path = testing_directory + '/' + blog_id + '.xml'
        with_id.write(blog_id + '\n')
        towrite.write(format_to_libsvm(map_unigrams(path, top_words), True) + '\n')
        completed += 1
        if (completed % 30) == 0:
            print '%.2f' % (completed*100/float(n)) + '% of testing data written.'


def label_testing_set_nrc(testing_directory):
    blog_directory = testing_directory
    dict1 = 'nrc.txt'
    t = Tagger(dict1)
    t.tag_directory(blog_directory)
    id_list = get_list_of_ids_for_testing('testing_ids.txt')
    towrite = open('labeled_testing', 'w')
    for i in range(10):
        t.score_nrc_from_list(id_list, True, i, 0.25, 100)
        toread = open('id_scored.txt')
        towrite.write(emotions[i] + '\n')
        for line in toread:
            towrite.write(line)
        towrite.write('\n')
        toread.close()
    towrite.close()


def extract_similarity(top_words):
    def cosine_similarity(vec1, vec2):
        dot = 0
        magA = 0
        magB = 0
        for value in vec1:
            magA += (value**2)
        for value in vec2:
            magB += (value**2)
        magA = math.sqrt(magA)
        magB = math.sqrt(magB)
        for i in range(len(vec1)):
            dot += (vec1[i] * vec2[i])
        return (dot/(magA * magB))
    f = open('vectors.txt')
    word2vec = {}
    similarity_matrix = {}
    # performance update multiple at once
    for line in f:
        tokens = line.split()
        if tokens[0] in top_words:
            vector = []
            for value in tokens[1:]:
                vector.append(float(value))
            #word2vec[tokens[0]] = vector
            # map index of word in top words list -> vector values
            word2vec[top_words.index(tokens[0])] = vector
    f.close()
    n = len(word2vec)
    completed = 0
    seen = []
    #print "Length of words in word2vec: " + str(n)
    for word0 in word2vec:
        similar_words = {}
        seen.append(word0)
        for wordN in word2vec:
            if wordN not in seen:
                vec1 = word2vec[word0]
                vec2 = word2vec[wordN]
                cos = cosine_similarity(vec1, vec2)
                if cos != 0:
                    
                    similar_words[wordN] = cos

        similarity_matrix[word0] = similar_words
        completed += 1
        if (completed % 3000) == 0:
             print '%.2f' % (completed*100/float(n)) + '% similarity_matrix completed.'
    return similarity_matrix


# def extract_top_labels(xml_directory, dictionary):
#     pass


def extract_top_labels(dict_path):
    top_words = []
    f = open(dict_path, 'r')
    if dict_path == 'nrc.txt':
        for line in f:
            tokens = line.split()
            word = tokens[0]
            top_words.append(word)
    f.close()
    return top_words


def extract_interval_features(xml_directory, dictionary):
    pass


def read_top_words(file_path):
    top_words = []
    f = open(file_path, 'r')
    for line in f:
        if len(line.split()) == 1:
            top_words.append(line.split()[0].lower())
    f.close()
    return top_words


def extract_top_words(xml_directory):
    words = {}
    top_words = []
    files = os.listdir(xml_directory)
    n = len(files)
    completed = 0
    for f in files:
            if f.endswith('.xml'):
                file_path = xml_directory + '/' + f
                f = open(file_path, 'r')
                for line in f:
                    if '<word>' in line:
                        begin = line.find('<word>') + 6
                        end = line.rfind('</word>')
                        word = line[begin:end]
                        if word in words:
                            words[word] = words[word] + 1
                        else:
                            words[word] = 1
                f.close()
                completed += 1
                if (completed % 1000) == 0:
                    print '%.2f' % (completed*100/float(n)) + '% top-words extraction finished.'
    # for word in words:
    #     if words[word] > 4:
    #         top_words.append(word)
    sorted_words = sorted(words.items(), key=operator.itemgetter(1))
    sorted_words = list(reversed(sorted_words))
    for i in range(2000):
        top_words.append(sorted_words[i][0])
    towrite = open('top_words.txt', 'w')
    for word in top_words:
        towrite.write(word + '\n')
    towrite.close()



def map_unigrams(xml_filename, top_words):
    feature_vector = []
    words_in_file = {}
    f = open(xml_filename, 'r')
    for line in f:
        if 'word' in line:
            begin = line.find('<word>') + 6
            end = line.rfind('</word>')
            word = line[begin:end]
            if word in words_in_file:
                words_in_file[word] = words_in_file[word] + 1
            else:
                words_in_file[word] = 1
    f.close()
    for word in top_words:
        if word in words_in_file:
            feature_vector.append(words_in_file[word])
        else:
            feature_vector.append(0)
    return feature_vector


def format_to_libsvm(feature_vector, is_label):
    values = ''
    for i in range(len(feature_vector)):
        if feature_vector[i] > 0:
            values += str(i+1) + ':' + str(feature_vector[i]) + ' '
    if is_label:
        values = '+1 ' + values
    else:
        values = '-1 ' + values
    return values
    

def get_list_of_ids_for_testing(path_name):
    ids = []
    f = open(path_name)
    for line in f:
        end = line.find('.txt')
        ids.append(line[0: end])
    f.close()
    return ids


def get_list_of_ids(path_name):
    ids = []
    f = open(path_name)
    for line in f:
        begin = line.find('(') + 2
        end = line.find(',') - 1
        ids.append(line[begin: end] + '.txt')
    f.close()
    return ids


def get_blogs_from_ids(output_file, id_list, blog_directory):
    id_to_entry = {}
    id_to_path = {}
    for (dir, _, files) in os.walk(blog_directory):
        for f in files:
            path = os.path.join(dir, f)
            if f in id_list:
                id_to_path[f] = path
                toopen = open(path, 'r')
                entry = ''
                for line in toopen:
                    entry += (line + '\n')
                toopen.close()
                id_to_entry[f] = entry
    towrite = open(output_file, 'w')
    for i in id_list:
        towrite.write(id_to_path[i] + '\n')
        towrite.write(id_to_entry[i] + '\n')
    towrite.close()