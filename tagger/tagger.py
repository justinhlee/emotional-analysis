import os
import operator


class Tagger:

    def __init__(self, dict_path):
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
        f = open(dict_path, 'r')
        if dict_path == 'nrc.txt':
            for line in f:
                tokens = line.split()
                word = tokens[0]
                if word in self.dictionary:
                    values = self.dictionary[word]
                    self.dictionary[word] += (tokens[2])
                else:
                    self.dictionary[word] = [tokens[2]]
            f.close()
        if dict_path == 'anew.txt':
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
        count = 0
        for f in os.listdir(directory_path):
            if f.endswith('.xml'):
                self.tag_entry(directory_path + '/' + f)
            count += 1
            if (count % 1000) == 0:
                print str(count) + ' entries tagged.'


    # def score_valence(self, from_highest):
    #     self.valence_scores = {}
    #     sorted_entries = []
    #     for entry_id in self.entries:
    #         entry = self.entries[entry_id]
    #         lemmas = entry.get_tagged_words()
    #         score = 0
    #         sum_val = 0
    #         min_valence = 10
    #         max_valence = 0
    #         for lemma in lemmas:
    #             value = float(self.dictionary[lemma][0])
    #             # get range
    #             if (value < min_valence):
    #                 min_valence = value
    #             if (value > max_valence):
    #                 max_valence = value
    #             sum_val += value
    #         emotion_range = max_valence - min_valence
    #         n = len(lemmas)
    #         if (n > 0):
    #             score = sum_val/(len(lemmas))
    #         if from_highest:
    #             if (emotion_range < 2) and (score > 8):
    #                 self.valence_scores[entry_id] = score
    #         else:
    #             if (score > 0) and (score < 3):
    #                 self.valence_scores[entry_id] = score
    #     sorted_entries = sorted(self.valence_scores.items(), key=operator.itemgetter(1))
    #     # doesn't matter to sort the list when they're all training
    #     sorted_entries = list(reversed(sorted_entries))
    #     towrite = open('id_scored_valence.txt', 'w')
    #     for i in range(len(sorted_entries)):
    #         towrite.write(str(sorted_entries[i]) + '\n')

    # threshold is some value from (0, 1]
    def score_nrc(self, from_highest, emotion_id, threshold, max_count):
        # anger 0
        # anticipation 1
        # disgust 2
        # fear 3
        # joy 4
        # negative 5
        # positive 6
        # sadness 7
        # surprise 8
        # trust 9
        scores = {}
        count = 0
        for entry_id in self.entries:
            entry = self.entries[entry_id]
            lemmas = entry.get_tagged_words()
            score = 0
            sum_val = 0
            for lemma in lemmas:
                value = float(self.dictionary[lemma][emotion_id])
                sum_val += value
            n = len(lemmas)
            if (n > 0):
                score = sum_val/(float(len(lemmas)))
            if from_highest:
                if (score > threshold):
                    scores[entry_id] = score
                    count += 1
            else:
                if (score == 0):
                    scores[entry_id] = score
                    count += 1
            if count > max_count:
                break
        sorted_entries = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_entries = list(reversed(sorted_entries))
        towrite = open('id_scored.txt', 'w')
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
