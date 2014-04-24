__author__ = 'Rituparna'

import Memorability_Training as mtr

class Test():
    def __init__(self):
        self.testfile    = 'test.txt'
        self.testparsed  = 'test.dat'

    def memorability_test(self, parsed_file, test_file):
        #Reading the test file and creating the feature file for that
        mtr.readfile(test_file ,parsed_file)
        mtr.buildQuoteDictionaries(parsed_file)
        mtr.buildFeatureFile(test_file)


#Create feature vector for the testing data
test = Test()
test.memorability_test(test.testparsed, test.testfile)