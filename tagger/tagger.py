import os
import operator


def extract_top_words(xml_directory):
    words = []
    for f in os.listdir(xml_directory):
            if f.endswith('.xml'):
                file_path = xml_directory + '/' + f
                f = open(file_path, 'r')
                for line in f:
                    if 'word' in line:
                        begin = line.find('<word>') + 6
                        end = line.rfind('</word>')
                        words.append(line[begin:end])
                f.close()
    return list(set(words))


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

def format_to_libsvm(feature_vector):
    for i in range(len(feature_vector)):
        if feature_vector[i] != 0:
            print str(i+1) + ':' + str(feature_vector[i])


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


class Tagger:

    def __init__(self, dict_path, d_name):
        # pass in the dictionary to use for tagging
        # Valence - unpleasant ---- pleasant
        # Arousal - Calm ------ Excited
        # Dominance/Control
        # Word  Wdnum   ValMn   ValSD   AroMn   AroSD   DomMn   DomSD
        #  0      1      2        3       4       5      6       7
        # Dictionary: Word -> [Values: Mean Valence, Mean Arousal, Mean Dominance]
        # Entries: ID -> Blog Entries
        # Weighted Entries: ID -> Emotion Words/Total Words percentage
        # coverage: ID -> Emotion Lemma/Total Lemmas percentage
        # occurences: ID -> # Dictionary Occurrences
        # valence_scores: ID -> valence score
        self.dictionary = {}
        self.entries = {}
        self.coverage = {}
        self.occurrences = {}
        self.sorted_weighted = []
        self.sorted_absolute = []
        self.valence_scores = {}
        f = open(dict_path, 'r')
        if d_name == 'nrc':
            for line in f:
                tokens = line.split()
                word = tokens[0]
                if word in self.dictionary:
                    values = self.dictionary[word]
                    self.dictionary[word] += (tokens[2])
                else:
                    self.dictionary[word] = [tokens[2]]
            f.close()
        if d_name == 'anew':
            for line in f:
                tokens = line.split()
                values = [tokens[2], tokens[4], tokens[6]]
                self.dictionary[tokens[0]] = values
            f.close()
    
    def tag_entry(self, entry_path):
        f = open(entry_path, 'r')
        begin = entry_path.find('/') + 1
        end = entry_path.find('.')
        entry_id = entry_path[begin:end]
        lemmas = []
        tagged_words = {}
        lemma_count = {}
        for line in f:
            if 'lemma' in line:
                begin = line.find('<lemma>') + 7
                end = line.rfind('</lemma>')
                lemmas.append(line[begin:end])
        # annotate the lemmas contained in the dictionary
        # store counts
        for lemma in lemmas:
            if lemma in self.dictionary:
                tagged_words[lemma] = self.dictionary[lemma]
                if lemma in lemma_count:
                    lemma_count[lemma] += 1
                else:
                    lemma_count[lemma] = 1
        # create BlogEntry instance
        entry = BlogEntry(lemmas, tagged_words, entry_id)
        self.entries[entry_id] = entry
        self.coverage[entry_id] = entry.get_coverage()
        self.occurrences[entry_id] = entry.get_occurrences()
        f.close()

    def tag_directory(self, directory_path):
        for f in os.listdir(directory_path):
            if f.endswith('.xml'):
                self.tag_entry(directory_path + '/' + f)

    def score_valence(self):
        for entry_id in self.entries:
            entry = self.entries[entry_id]
            lemmas = entry.get_tagged_words()
            score = 0
            sum_val = 0
            min_valence = 10
            max_valence = 0
            for lemma in lemmas:
                value = float(self.dictionary[lemma][0])
                # get range
                if (value < min_valence):
                    min_valence = value
                if (value > max_valence):
                    max_valence = value
                sum_val += value
            emotion_range = max_valence - min_valence
            n = len(lemmas)
            if (n > 0):
                score = sum_val/(len(lemmas))
            if (emotion_range < 1) and (score > 7):
                self.valence_scores[entry_id] = score
            if (emotion_range < 2) and (score < 4) and (score > 0):
                self.valence_scores[entry_id] = score
        sorted_entries = sorted(self.valence_scores.items(), key=operator.itemgetter(1))
        sorted_entries = list(reversed(sorted_entries))
        towrite = open('id_scored_valence.txt', 'w')
        for i in range(len(sorted_entries)):
            towrite.write(str(sorted_entries[i]) + '\n')

    def score_joy(self):
        for entry_id in self.entries:
            entry = self.entries[entry_id]
            lemmas = entry.get_tagged_words()
            score = 0
            sum_val = 0
            for lemma in lemmas:
                value = float(self.dictionary[lemma][4])
                sum_val += value
            n = len(lemmas)
            if (n > 0):
                score = sum_val/(float(len(lemmas)))
            if (score > 0):
                self.valence_scores[entry_id] = score
        sorted_entries = sorted(self.valence_scores.items(), key=operator.itemgetter(1))
        sorted_entries = list(reversed(sorted_entries))
        towrite = open('id_scored_joy.txt', 'w')
        for i in range(len(sorted_entries)):
            towrite.write(str(sorted_entries[i]) + '\n')
        
    
    def get_high_occurrence_blogs(self, n):
        if not self.sorted_absolute:
            sorted_entries = sorted(self.occurrences.items(), key=operator.itemgetter(1))
            self.sorted_absolute = list(reversed(sorted_entries))
        towrite = open('id_occurrences.txt', 'w')
        for i in range(n):
            towrite.write(str(self.sorted_absolute[i]) + '\n')

    def get_high_coverage_blogs(self, n):
        if not self.sorted_weighted:
            sorted_entries = sorted(self.coverage.items(), key=operator.itemgetter(1))
            self.sorted_weighted = list(reversed(sorted_entries))
        towrite = open('id_coverage.txt', 'w')
        for i in range(n):
            t = self.sorted_weighted[i]
            towrite.write(str(t) + '\n')

    def get_tagged_from_high_occurence(self, n):
        if not self.sorted_absolute:
            sorted_entries = sorted(self.occurrences.items(), key=operator.itemgetter(1))
            self.sorted_absolute = list(reversed(sorted_entries))
        towrite = open('tagged_high_occurrence.txt', 'w')
        for i in range(n):
            t = self.sorted_absolute[i]
            entry = self.entries[t[0]]
            towrite.write(str(t) + '\n')
            for word in entry.get_tagged_words():
                towrite.write(word + ': ' + str(self.dictionary[word]) + '\n')
    
    def get_tagged_from_high_coverage(self, n):
        if not self.sorted_weighted:
            sorted_entries = sorted(self.coverage.items(), key=operator.itemgetter(1))
            self.sorted_weighted = list(reversed(sorted_entries))
        towrite = open('tagged_high_coverage.txt', 'w')
        for i in range(n):
            t = self.sorted_weighted[i]
            entry = self.entries[t[0]]
            towrite.write(str(t) + '\n')
            for word in entry.get_tagged_words():
                towrite.write(word + ': ' + str(self.dictionary[word]) + '\n')

    def get_blog_by_id(self, id):
        blog = self.entries[id]
        return blog.get_tagged_words()


class BlogEntry:

    def __init__(self, all_words, tagged_words, id):
        # represent each blog entry as a bag of words
        # have scores absolute scores
        self.id = id
        self.words = all_words
        tagged = []
        n = 0
        for lemma in all_words:
            if lemma in tagged_words:
                n += 1
                tagged.append(lemma)
        self.tagged_words = tagged
        self.occurrences = n
        self.coverage = n/float(len(all_words))

    def get_coverage(self):
        return self.coverage

    def get_occurrences(self):
        return self.occurrences

    def get_all_words(self):
        return self.words

    def get_tagged_words(self):
        return self.tagged_words
