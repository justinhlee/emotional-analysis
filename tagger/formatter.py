import os
import operator
import math


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



def extract_top_words(xml_directory):
    # TODO: Get only words with at least five counts, or some way to cut down feature size
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
    for word in words:
        if words[word] > 4:
            top_words.append(word)

    # sorted_words = sorted(words.items(), key=operator.itemgetter(1))
    # sorted_words = list(reversed(sorted_words))
    # for i in range(2000):
    #     top_words.append(sorted_words[i][0])
    return top_words


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