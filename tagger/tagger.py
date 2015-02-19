import os
import operator


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

    def __init__(self, dict_list):
        #pass in the dictionary list to use for tagging
        # Valence - unpleasant ---- pleasant
        # Arousal - Calm ------ Excited
        # Dominance/Control
        # Word  Wdnum   ValMn   ValSD   AroMn   AroSD   DomMn   DomSD
        #  0      1      2        3       4       5      6       7
        # Dictionary: Word -> [Values (Mean Valence, Mean Arousal, Mean Dominance)]
        # Entries: ID -> Blog Entries
        # Weighted Entries: ID -> Emotion Words/Total Words percentage
        self.dictionary = {}
        self.entries = {}
        self.weighted_scores = {}
        self.absolute_scores = {}
        self.sorted_weighted = []
        self.sorted_absolute = []

        for dict_path in dict_list:
            f = open(dict_path, 'r')
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
        for line in f:
            if 'lemma' in line:
                begin = line.find('<lemma>') + 7
                end = line.rfind('</lemma>')
                lemmas.append(line[begin:end])
        # annotate the lemmas contained in the dictionary
        for lemma in lemmas:
            if lemma in self.dictionary:
                tagged_words[lemma] = self.dictionary[lemma]

        entry = BlogEntry(lemmas, tagged_words, entry_id)
        self.entries[entry_id] = entry
        self.weighted_scores[entry_id] = entry.get_weighted_score()
        self.absolute_scores[entry_id] = entry.get_absolute_score()
        f.close()

    def tag_directory(self, directory_path):
        for f in os.listdir(directory_path):
            if f.endswith('.xml'):
                self.tag_entry(directory_path + '/' + f)

    def get_high_scored_blogs(self, n):
        if not self.sorted_absolute:
            sorted_entries = sorted(self.absolute_scores.items(), key=operator.itemgetter(1))
            self.sorted_absolute = list(reversed(sorted_entries))
        towrite = open('training_absolute.txt', 'w')
        for i in range(n):
            towrite.write(str(self.sorted_absolute[i]) + '\n')

    def get_dense_scored_blogs(self, n):
        if not self.sorted_weighted:
            sorted_entries = sorted(self.weighted_scores.items(), key=operator.itemgetter(1))
            self.sorted_weighted = list(reversed(sorted_entries))
        towrite = open('training_normalized.txt', 'w')
        for i in range(n):
            t = self.sorted_weighted[i]
            towrite.write(str(t) + '\n')

    def get_blog_by_id(self, id):
        blog = self.entries[id]
        return blog.get_tagged_words()


class BlogEntry:

    def __init__(self, all_words, tagged_words, id):
        # represent each blog entry as a bag of words
        # have scores absolute scores
        self.id = id
        self.words = all_words
        self.tagged_words = tagged_words
        self.absolute_score = len(tagged_words)
        self.weighted_score = len(tagged_words)/float(len(all_words))

    def get_weighted_score(self):
        return self.weighted_score

    def get_absolute_score(self):
        return self.absolute_score

    def get_all_words(self):
        return self.words

    def get_tagged_words(self):
        return self.tagged_words
