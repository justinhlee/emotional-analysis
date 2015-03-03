from parser import *
import unittest


class parser_test(unittest.TestCase):

    def testOne(self):
        path = '../stories12.txt'
        path = '../icwsm09stories.txt'
        towrite = open('toprocess.txt', 'w')
        toread = open(path, 'r')
        for line in toread:
            # if "tiergroup-3/" in line or "tiergroup-2/" in line or "tiergroup-13/" in line:
            if "tiergroup-12/" in line or "tiergroup-11/" in line or "tiergroup-9/" in line:
                entry = ' '.join(line.split())
                towrite.write(entry + '\n')
        toread.close()
        towrite.close()

        path = 'toprocess.txt'

        p = Parser(path)
        p.process_xml()
        p.print_paths_to_file()

if __name__ == '__main__':
    unittest.main()
