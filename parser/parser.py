import csv
import os
import xml.etree.ElementTree as ET
import linecache
import errno


def mkdir_p(path):
    # http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Parser:

    def __init__(self, path):
        # initialize a dictionary of path names -> [tuple of line numbers]
        # where tuples denote where personal entry begins and ends
        self.locations = {}
        # location of the preprocessed blog entries
        self.entries_paths = []
        with open(path, 'r') as metadata:
            data = csv.reader(metadata, delimiter=' ')
            for entry in data:
                blog_path = entry[0]
                line_number = []
                for n in (range(1, len(entry))):
                    if '.' not in entry[n] and entry[n] != '':
                        line_number.append(entry[n])
                if blog_path in self.locations:
                    self.locations[blog_path].append(tuple(line_number))
                else:
                    self.locations[blog_path] = [tuple(line_number)]
            metadata.close()

    def get_locations(self):
        return self.locations

    def print_paths_to_file(self):
        f = open('entries.txt', 'w')
        for entry in self.entries_paths:
            f.write(entry + '\n')
        f.close()

    def print_to_file(self, entry, file_path, count):
        index = file_path.rfind('/')
        path_to_directory = file_path[:index]
        if not os.path.isdir(path_to_directory):
            mkdir_p(path_to_directory)
        output_file = path_to_directory + '/' + str(count) + '.txt'
        self.entries_paths.append(output_file)
        f = open(output_file, 'w')
        f.write(entry)
        f.close()

    def process_xml(self):
        xml_entries = []
        completed_paths = 0
        count = 0
        n = len(self.locations)
        for path in self.locations:
            # output a file per path
            line_numbers = self.locations[path]
            # edit adjusted path for current directory
            adjusted_path = '../../' + path
            for pair in line_numbers:
                entry = ''
                begin = int(float(pair[0]))
                end = int(float(pair[1])) + 1
                isDescription = False
                for line in range(begin, end):
                    current_line = linecache.getline(adjusted_path, line)
                    if isDescription:
                        entry += current_line
                        if '</description>' in current_line:
                            break
                    elif '<description' in current_line:
                        isDescription = True
                        entry += current_line
                xml_entries.append(entry)
                self.print_to_file(entry, 'entries/' + path, count)
                count += 1
            completed_paths += 1
            if (completed_paths % 10 == 0):
                print '%.2f' % (100*completed_paths/float(n)) + '% completed.'
