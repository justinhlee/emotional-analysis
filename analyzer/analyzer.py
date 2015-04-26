import os

'''

Dictionary:
Line Number -> Blog ID
Blog ID -> [anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]

directory_path is directory containing the LIBSVM output files to be analyzed
'''


class Analyzer:
    
    def __init__(self, blog_ids):
        self.line_id_map = {}
        self.line_vector_map = {}
        self.emotions = ['anger', 'anticipation', 'disgust', 'fear'
                        , 'joy', 'negative', 'positive', 'sadness'
                        , 'surprise', 'trust']
        with open(blog_ids) as f:
            for num, line in enumerate(f, 2):  # starts at 2 for LIBSVM first line
                self.line_id_map[num] = line.split()[0]
        for line_no in self.line_id_map:
            self.line_vector_map[line_no] = [0] * 10

    # takes probability output files from LIBSVM
    def count_multi_labels(self, directory_path):
        for f in os.listdir(directory_path):
            if 'output' in f:
                label_id = int(f[6])
                file_path = directory_path + '/' + f
                self.update(label_id, file_path)
        towrite = open('id_labels.txt', 'w')
        for num in self.line_vector_map:
            vector = self.line_vector_map[num]
            towrite.write(self.line_id_map[num] + '\n')
            for i in range(10):
                if int(vector[i]) == 1:
                    towrite.write(self.emotions[i] + '\n')
            towrite.write('\n')

    def percent_multi_labels(self):
        towrite = open('percent_labels.txt', 'w')
        for i in range(10):
            total = float(0)
            for num in self.line_vector_map:
                vector = self.line_vector_map[num]
                if int(vector[i]) == 1:
                    total += 1
            towrite.write(self.emotions[i] + ': ' + str(total*100/float(200)) + '% of the testing set \n')
            for j in range(10):
                count = 0
                for num in self.line_vector_map:
                    vector = self.line_vector_map[num]
                    if int(vector[j]) == 1 and int(vector[i]) == 1:
                        count += 1
                towrite.write(self.emotions[j] + ': ' + str(count*100/total) + '% \n')
            towrite.write('\n')
              
    def update(self, label_id, file_path):
        f = open(file_path, 'r')
        f.readline()
        for num, line in enumerate(f, 2):
            values = line.split()
            to_update = self.line_vector_map[num]
            to_update[label_id] = values[0]
            self.line_vector_map[num] = to_update
        f.close()
            




