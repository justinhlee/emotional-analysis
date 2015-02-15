import os
import operator

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
        for i in range(n):
            print self.sorted_absolute[i]

    def get_dense_scored_blogs(self, n):
        if not self.sorted_weighted:
            sorted_entries = sorted(self.weighted_scores.items(), key=operator.itemgetter(1))
            self.sorted_weighted  = list(reversed(sorted_entries))
        for i in range(n):
            print self.sorted_weighted[i]

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
