'''
Created on Jan 19, 2013

@author: mandar
'''

import argparse

STR_NUM_OF_PROTOTYPES = "num_of_prototypes"
NUM_OF_PROTOTYPES = "num_of_prototypes"

STR_PROTOTYPE_GEN_METHOD = "prototype generation method"
PROTOTYPE_GEN_METHOD = "prototype_generation_method"

STR_TRAINING_ACCURACY = "SVM: training accuracy:"
BACK_SVM_TRAINING_ACCURACY = "back-svm-training-accuracy"
FRONT_SVM_TRAINING_ACCURACY = "front-svm-training-accuracy"
LEFT_SVM_TRAINING_ACCURACY = "left-svm-training-accuracy"
RIGHT_SVM_TRAINING_ACCURACY = "right-svm-training-accuracy"

STR_TEST_ACCURACY = "test accuracy:"
AGGREGATE_TESTING_ACCURACY = "aggregate-test-accuracy"

class StdoutDataExtractor(object):

    def __init__(self, stdout_file):

        self.stdout_file = stdout_file

        self.lines = None        
        self.data_dict = {}
        
    def load_data(self):
        
        stdout_file = open(self.stdout_file, "r")
        self.lines = stdout_file.readlines()
        stdout_file.close()
        
    def _parse_data(self):
        
        train_acc_list = []
        
        for line in self.lines:
            csv = line.split(":")
            if STR_NUM_OF_PROTOTYPES in line:
                self.data_dict[STR_NUM_OF_PROTOTYPES] = float(csv[1])
                continue
            if STR_PROTOTYPE_GEN_METHOD in line:
                self.data_dict[PROTOTYPE_GEN_METHOD] = csv[1]
                continue
            if STR_TRAINING_ACCURACY in line:
                train_acc_list.append(float(csv[2]))
                continue
            if STR_TEST_ACCURACY in line:
                self.data_dict[AGGREGATE_TESTING_ACCURACY] = float(csv[1])
                continue
        
        self.data_dict[BACK_SVM_TRAINING_ACCURACY] = train_acc_list[0]
        self.data_dict[FRONT_SVM_TRAINING_ACCURACY] = train_acc_list[1]
        self.data_dict[LEFT_SVM_TRAINING_ACCURACY] = train_acc_list[2]
        self.data_dict[RIGHT_SVM_TRAINING_ACCURACY] = train_acc_list[3]

    def get_data_dict(self):
        
        self._parse_data()
        
        return self.data_dict
    
    def print_data_dict(self):
        
        for key in self.data_dict:
            print key + ":\t " + str(self.data_dict[key])
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='stdout.txt file parser')
    parser.add_argument("-f", "--stdout-file", required=True, type=str, action="store",
                        dest='stdout_file', help='stdout.txt file path')
    args = parser.parse_args()
    
    stdout_parser = StdoutDataExtractor(args.stdout_file)
    stdout_parser.load_data()
    data_dict = stdout_parser.get_data_dict()
    stdout_parser.print_data_dict()
