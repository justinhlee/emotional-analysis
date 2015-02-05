import csv
import os
import xml.etree.ElementTree as ET
import linecache


class Parser:

    def __init__(self, path):
        # initialize a dictionary of path names -> [tuple of line numbers]
        # where tuples denote where personal entry begins and ends
        self.locations = {}
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

    def get_locations(self):
        return self.locations

    def process_xml(self):
        xml_entries = []
        for path in self.locations:
            line_numbers = self.locations[path]
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

        for i in range(1000):
            print xml_entries[i]
            print '='*100

        
    def tokenize(self):
        pass
           

