import os

'''

Dictionary:
blog_csv is csv format for NRC results

id_labels
Blog Entry ID -> Assigned Emotion id_labels

emotion_ids
NRC Emotion -> List of blog entry IDs that were labeled as that emotions

'''


class Reader:
    
    def __init__(self, blog_csv):
        self.id_labels_map = {}
        self.emotion_ids_map = {}

        self.emotions = ['anger', 'anticipation', 'disgust', 'fear'
                        , 'joy', 'negative', 'positive', 'sadness'
                        , 'surprise', 'trust']
        f = open(blog_csv, 'r')
        for line in f:
            tokens = line.split()
            values = []
            for value in tokens[1:]:
                values.append(int(value))
            self.id_labels_map[tokens[0]] = values
    
    def count_label(self, emotion_id):
        count = 0
        ids = []
        for entry in self.id_labels_map:
            values = self.id_labels_map[entry]
            if values[emotion_id] == 1:
                ids.append(entry)
                count += 1
        #print self.emotions[emotion_id] + ' ' + str(count)
        emotion = self.emotions[emotion_id]
        self.emotion_ids_map[emotion] = ids
        return count

    def count_multi_labels(self):
        counts = []
        for i in range(10):
            counts.append(self.count_label(i))

        for first_emotion in range(10):
            emotion = self.emotions[first_emotion]
            entries_that_contain_first_emotion = self.emotion_ids_map[emotion]
            for second_emotion in range(10):
                second_emotion_count = 0
                for entry in entries_that_contain_first_emotion:
                    labels_list = self.id_labels_map[entry]
                    if labels_list[second_emotion] == 1:
                        second_emotion_count += 1
                
                #print self.emotions[second_emotion], self.emotions[first_emotion] + ' ' +  '%.2f' % (float(second_emotion_count)*100/len(self.id_labels_map)) + '%'
                if len(entries_that_contain_first_emotion) != 0:
                    print self.emotions[second_emotion], self.emotions[first_emotion] + ' ' + '%.2f' %  (float(second_emotion_count)*100/len(entries_that_contain_first_emotion)) + '%'
                #print second_emotion_count, len(entries_that_contain_first_emotion)
            print '====='






        # for i in range(10):
        #     coemotion = self.emotions[i]
        #     for emotion in self.emotion_ids_map:
        #         ids = self.emotion_ids_map[emotion]
        #         coemotion_count = 0
        #         for entry in ids:
        #             current_labels = self.id_labels_map[entry]

        #             if current_labels[i] == 1:
        #                 coemotion_count += 1
        #         print coemotion, emotion
        #         print coemotion_count, len(ids)

        #     print '===='

                #print emotion, self.emotion_ids_map[emotion]



        # with open(blog_ids) as f:
        #     for num, line in enumerate(f, 2):  # starts at 2 for LIBSVM first line
        #         self.line_id_map[num] = line.split()[0]
        # for line_no in self.line_id_map:
        #     self.line_vector_map[line_no] = [0] * 10

    # takes probability output files from LIBSVM
    '''
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
    '''




