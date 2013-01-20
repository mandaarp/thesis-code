#!/usr/bin/env python
'''
Created on Jan 19, 2013

@author: mandar
'''


import sys,os
source_path = os.path.join(os.environ['HOME'],"thesis-code")
if source_path not in sys.path:
    sys.path.insert(0,source_path)

import argparse
from automation import stdout_data_extractor as StdoutParser
from experimental_code import svm_wise_test_accuracy as script

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='SVM analyzer with train-acc-linear method')
    parser.add_argument("-sf", "--stdout-file", required=True, type=str, action="store",
                        dest='stdout_file', help='stdout.txt file path')
    parser.add_argument("-df", "--decision-values-file", required=True, type=str, action="store",
                        dest="decision_values_file", help="decision_values.csv file path")
    args = parser.parse_args()
    
    stdout_parser = StdoutParser.StdoutDataExtractor(args.stdout_file)
    stdout_parser.load_data()
    data_dict = stdout_parser.get_data_dict()
    
    svm_analyzer = script.SVMAnalysis(args.decision_values_file)
    svm_analyzer.load_data()
    svm_analyzer.set_training_accuracies(float(data_dict[StdoutParser.BACK_SVM_TRAINING_ACCURACY]),
                                         float(data_dict[StdoutParser.FRONT_SVM_TRAINING_ACCURACY]),
                                         float(data_dict[StdoutParser.LEFT_SVM_TRAINING_ACCURACY]),
                                         float(data_dict[StdoutParser.RIGHT_SVM_TRAINING_ACCURACY]))
#    svm_analyzer.set_training_accuracies(0.90375, 0.876875, 0.874375, 0.888125)
    svm_analyzer.train_acc_linear_decision_function()
    test_accuracy = svm_analyzer.aggregate_test_accuracy()
    print "Aggregate test accuracy: " + str(test_accuracy)