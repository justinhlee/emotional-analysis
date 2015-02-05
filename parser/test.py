from parser import *
import unittest


class parser_test(unittest.TestCase):

    def testOne(self):
        path = '../stories12.txt'
        p = Parser(path)
        p.process_xml()
        



if __name__ == '__main__':
    unittest.main()
