'''
Created on Jan 19, 2013

@author: mandar
'''

import sys,os
source_path = os.path.join(os.environ['HOME'],"thesis-code")
if source_path not in sys.path:
    sys.path.insert(0,source_path)
    
import argparse
import numpy
from experimental_code.one_vs_one import Constants as one_vs_one_value

STR_PEDESTRIAN_BACK = "pedestrian-back"
STR_PEDESTRIAN_FRONT = "pedestrian-front"
STR_PEDESTRIAN_LEFT = "pedestrian-left"
STR_PEDESTRIAN_RIGHT = "pedestrian-right"
STR_TEST_TYPE_ONE_VS_ONE = "one-vs-one"
STR_TEST_TYPE_ONE_VS_ALL = "one-vs-all"
EVAL_TRAIN_ACC_LINEAR = "train-acc-linear"

class SVMAnalysis(object):
    '''
    classdocs
    '''
    def __init__(self, decision_values_file):
        '''
        Constructor
        '''
        self.decision_values_file = decision_values_file
        self.lines = None
        
        self.back_svm_image_to_decision_value = {}
        self.front_svm_image_to_decision_value = {}
        self.left_svm_image_to_decision_value = {}
        self.right_svm_image_to_decision_value = {}
        
        self.back_vs_front_image_to_decision_value = {}
        self.back_vs_left_image_to_decision_value = {}
        self.back_vs_right_image_to_decision_value = {}
        self.front_vs_left_image_to_decision_value = {}
        self.front_vs_right_image_to_decision_value = {}
        self.left_vs_right_image_to_decision_value = {}
        
        self.back_svm_predictions = {}
        self.front_svm_predictions = {}
        self.left_svm_predictions = {}
        self.right_svm_predictions = {}
        
        self.back_vs_front_svm_predictions = {}
        self.back_vs_left_svm_predictions = {}
        self.back_vs_right_svm_predictions = {}
        self.front_vs_left_svm_predictions = {}
        self.front_vs_right_svm_predictions = {}
        self.left_vs_right_svm_predictions = {}
        
        self.back_svm_image_to_decision_value_train_acc_linear = {}
        self.front_svm_image_to_decision_value_train_acc_linear = {}
        self.left_svm_image_to_decision_value_train_acc_linear = {}
        self.right_svm_image_to_decision_value_train_acc_linear = {}
        
        self.back_svm_training_accuracy = None
        self.front_svm_training_accuracy = None
        self.left_svm_training_accuracy = None
        self.right_svm_training_accuracy = None
        
        self.aggregate_predictions = {}
        
    def load_data(self, test_type=STR_TEST_TYPE_ONE_VS_ALL):
        
        decision_values_file = open(self.decision_values_file, "r")
        self.lines = decision_values_file.readlines()
        decision_values_file.close()
        
        for line in self.lines[1:]:
            csv = line.split(',')
            if test_type == STR_TEST_TYPE_ONE_VS_ALL:
                self.back_svm_image_to_decision_value[csv[0]]=float(csv[1])
                self.front_svm_image_to_decision_value[csv[0]]=float(csv[2])
                self.left_svm_image_to_decision_value[csv[0]]=float(csv[3])
                self.right_svm_image_to_decision_value[csv[0]]=float(csv[4])
                
            elif test_type == STR_TEST_TYPE_ONE_VS_ONE:
                self.back_vs_front_image_to_decision_value[csv[0]]=float(csv[1])
                self.back_vs_left_image_to_decision_value[csv[0]]=float(csv[2])
                self.back_vs_right_image_to_decision_value[csv[0]]=float(csv[3])
                self.front_vs_left_image_to_decision_value[csv[0]]=float(csv[4])
                self.front_vs_right_image_to_decision_value[csv[0]]=float(csv[5])
                self.left_vs_right_image_to_decision_value[csv[0]]=float(csv[6])
            else:
                print "invalid test type!!!\n valid test types: one-vs-all, one-vs-one"
        
    def set_training_accuracies(self, back, front, left, right):
        self.back_svm_training_accuracy = float(back)
        self.front_svm_training_accuracy = float(front)
        self.left_svm_training_accuracy = float(left)
        self.right_svm_training_accuracy = float(right)
        
    def _test_svm(self, image_to_decision_value):
        
        actual_to_predicted = {}
        
        for image in image_to_decision_value:
            if image_to_decision_value[image] > 0:
                actual_to_predicted[image] = 1;
            else:
                actual_to_predicted[image] = -1;
                
        return actual_to_predicted

    def generate_svm_results(self, test_type=STR_TEST_TYPE_ONE_VS_ALL):
        
        if test_type == STR_TEST_TYPE_ONE_VS_ALL:
            self.back_svm_predictions = self._test_svm(self.back_svm_image_to_decision_value)
            self.front_svm_predictions = self._test_svm(self.front_svm_image_to_decision_value)
            self.left_svm_predictions = self._test_svm(self.left_svm_image_to_decision_value)
            self.right_svm_predictions = self._test_svm(self.right_svm_image_to_decision_value)
        
        elif test_type == STR_TEST_TYPE_ONE_VS_ONE:
            self.back_vs_front_svm_predictions = self._test_svm(self.back_vs_front_image_to_decision_value)
            self.back_vs_left_svm_predictions = self._test_svm(self.back_vs_left_image_to_decision_value)
            self.back_vs_right_svm_predictions = self._test_svm(self.back_vs_right_image_to_decision_value)
            self.front_vs_left_svm_predictions = self._test_svm(self.front_vs_left_image_to_decision_value)
            self.front_vs_right_svm_predictions = self._test_svm(self.front_vs_right_image_to_decision_value)
            self.left_vs_right_svm_predictions = self._test_svm(self.left_vs_right_image_to_decision_value)
        
        else:
            print "invalid test type!!!\n valid test types: one-vs-all, one-vs-one"
    
    def _get_test_accuracy(self, svm_predictions, actual_class):
        
        true_predictions = 0
        
        for prediction in svm_predictions:
            if svm_predictions[prediction] == 1 and actual_class in prediction:
                true_predictions = true_predictions + 1
            elif svm_predictions[prediction] == -1 and actual_class not in prediction:
                true_predictions = true_predictions + 1
        
        return float((float(true_predictions) / float(len(svm_predictions)))*100.0)
    
    def _get_test_accuracy_one_vs_one(self, svm_predictions, positive_class, negative_class):
        
        true_predictions = 0
        
        for prediction in svm_predictions:
            if svm_predictions[prediction] == 1 and positive_class in prediction:
                true_predictions = true_predictions + 1
            elif svm_predictions[prediction] == -1 and negative_class in prediction:
                true_predictions = true_predictions + 1
        
        return float((float(true_predictions) / float(len(svm_predictions))) * 100.0)
        
    def svm_wise_test_accuracies(self, test_type=STR_TEST_TYPE_ONE_VS_ALL):
        
        print "calculating test accuracies ..."
        if test_type == STR_TEST_TYPE_ONE_VS_ALL:
            back_svm_test_accuracy = self._get_test_accuracy(self.back_svm_predictions, STR_PEDESTRIAN_BACK)
            front_svm_test_accuracy = self._get_test_accuracy(self.front_svm_predictions, STR_PEDESTRIAN_FRONT)
            left_svm_test_accuracy = self._get_test_accuracy(self.left_svm_predictions, STR_PEDESTRIAN_LEFT)
            right_svm_test_accuracy = self._get_test_accuracy(self.right_svm_predictions, STR_PEDESTRIAN_RIGHT)
        
            print STR_PEDESTRIAN_BACK + ": " + str(back_svm_test_accuracy) + " %"
            print STR_PEDESTRIAN_FRONT + ": " + str(front_svm_test_accuracy) + " %"
            print STR_PEDESTRIAN_LEFT + ": " + str(left_svm_test_accuracy) + " %"
            print STR_PEDESTRIAN_RIGHT + ": " + str(right_svm_test_accuracy) + " %"
        
        elif test_type == STR_TEST_TYPE_ONE_VS_ONE:
            back_vs_front_test_accuracy = self._get_test_accuracy_one_vs_one(self.back_vs_front_svm_predictions,
                                                                             STR_PEDESTRIAN_BACK, STR_PEDESTRIAN_FRONT)
            back_vs_left_test_accuracy = self._get_test_accuracy_one_vs_one(self.back_vs_left_svm_predictions,
                                                                             STR_PEDESTRIAN_BACK, STR_PEDESTRIAN_LEFT)
            back_vs_right_test_accuracy = self._get_test_accuracy_one_vs_one(self.back_vs_right_svm_predictions,
                                                                             STR_PEDESTRIAN_BACK, STR_PEDESTRIAN_RIGHT)
            front_vs_left_test_accuracy = self._get_test_accuracy_one_vs_one(self.front_vs_left_svm_predictions,
                                                                             STR_PEDESTRIAN_FRONT, STR_PEDESTRIAN_LEFT)
            front_vs_right_test_accuracy = self._get_test_accuracy_one_vs_one(self.front_vs_right_svm_predictions,
                                                                             STR_PEDESTRIAN_FRONT, STR_PEDESTRIAN_RIGHT)
            left_vs_right_test_accuracy = self._get_test_accuracy_one_vs_one(self.left_vs_right_svm_predictions,
                                                                             STR_PEDESTRIAN_LEFT, STR_PEDESTRIAN_RIGHT)
            
            print one_vs_one_value.STR_PEDESTRIAN_BACK_VS_FRONT + ": " + str(back_vs_front_test_accuracy) + " %"
            print one_vs_one_value.STR_PEDESTRIAN_BACK_VS_LEFT + ": " + str(back_vs_left_test_accuracy) + " %"
            print one_vs_one_value.STR_PEDESTRIAN_BACK_VS_RIGHT + ": " + str(back_vs_right_test_accuracy) + " %"
            print one_vs_one_value.STR_PEDESTRIAN_FRONT_VS_LEFT + ": " + str(front_vs_left_test_accuracy) + " %"
            print one_vs_one_value.STR_PEDESTRIAN_FRONT_VS_RIGHT + ": " + str(front_vs_right_test_accuracy) + " %"
            print one_vs_one_value.STR_PEDESTRIAN_LEFT_VS_RIGHT + ": " + str(left_vs_right_test_accuracy) + " %"
        else:
            print "invalid test type!!!\n valid test types: one-vs-all, one-vs-one"
            
        print "test accuracy calculation completed"
        
        
    
    def _argmax(self, numpy_array=None):
        
        max_value_index = numpy_array.argmax()

        if max_value_index == 0:
            return STR_PEDESTRIAN_BACK
        elif max_value_index == 1:
            return STR_PEDESTRIAN_FRONT
        elif max_value_index == 2:
            return STR_PEDESTRIAN_LEFT
        elif max_value_index == 3:
            return STR_PEDESTRIAN_RIGHT
        
    def _update_dec_values_train_acc_linear(self, image_to_decision_value):
        
        for key in image_to_decision_value:
            old = image_to_decision_value[key]
            new = 0
            if STR_PEDESTRIAN_BACK in key:
                image_to_decision_value[key] = float(self.back_svm_training_accuracy * image_to_decision_value[key])
                new = image_to_decision_value[key]
            elif STR_PEDESTRIAN_FRONT in key:
                image_to_decision_value[key] = float(self.front_svm_training_accuracy * image_to_decision_value[key])
                new = image_to_decision_value[key]
            elif STR_PEDESTRIAN_LEFT in key:
                image_to_decision_value[key] = float(self.left_svm_training_accuracy * image_to_decision_value[key])
                new = image_to_decision_value[key]
            elif STR_PEDESTRIAN_RIGHT in key:
                image_to_decision_value[key] = float(self.right_svm_training_accuracy * image_to_decision_value[key])
                new = image_to_decision_value[key]
#            print "old: " + str(old) + " \t new: " + str(new)
        return image_to_decision_value
    
    def train_acc_linear_decision_function(self):
        
        self.back_svm_image_to_decision_value_train_acc_linear = self._update_dec_values_train_acc_linear(self.back_svm_image_to_decision_value)
        self.front_svm_image_to_decision_value_train_acc_linear = self._update_dec_values_train_acc_linear(self.front_svm_image_to_decision_value)
        self.left_svm_image_to_decision_value_train_acc_linear = self._update_dec_values_train_acc_linear(self.left_svm_image_to_decision_value)
        self.right_svm_image_to_decision_value_train_acc_linear = self._update_dec_values_train_acc_linear(self.right_svm_image_to_decision_value)
        
        for image in self.back_svm_image_to_decision_value_train_acc_linear:
            self.aggregate_predictions[image] = self._argmax(numpy.array([self.back_svm_image_to_decision_value_train_acc_linear[image],
                                                                          self.front_svm_image_to_decision_value_train_acc_linear[image],
                                                                          self.left_svm_image_to_decision_value_train_acc_linear[image],
                                                                          self.right_svm_image_to_decision_value_train_acc_linear[image]]
                                                                         ))

    def aggregate_test_accuracy(self):
        
        true_predictions = 0
        
        for key in self.aggregate_predictions:
            if self.aggregate_predictions[key] in key:
                true_predictions = true_predictions + 1
        
        return float((float(true_predictions)/len(self.aggregate_predictions))*100.0)

        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='entry point to direction estimator')
    parser.add_argument("-f", "--decision-value-file", required=True, type=str, action="store",
                        dest='decision_value_file', help='decision_values.csv file path')
    parser.add_argument("-tt", "--test-type", required=False, type=str, action="store",
                        dest="test_type", help="test-type: one-to-all, one-vs-one")
    parser.add_argument('-m', "--evaluation-method", required=False, type=str, action="store",
                        dest="evaluation_method", help="evaluation method - None or " + EVAL_TRAIN_ACC_LINEAR)
    parser.add_argument("-tb", "--back-svm-train-acc", required=False, type=float, action="store",
                        dest="back_svm_train_acc", help="back-svm training accuracy")
    parser.add_argument("-tf", "--front-svm-train-acc", required=False, type=float, action="store",
                        dest="front_svm_train_acc", help="front-svm training accuracy")
    parser.add_argument("-tl", "--left-svm-train-acc", required=False, type=float, action="store",
                        dest="left_svm_train_acc", help="left-svm training accuracy")
    parser.add_argument("-tr", "--right-svm-train-acc", required=False, type=float, action="store",
                        dest="right_svm_train_acc", help="right-svm training accuracy")
    
    args = parser.parse_args()
    
    svm_analyzer = SVMAnalysis(args.decision_value_file)
    if args.test_type == STR_TEST_TYPE_ONE_VS_ONE:
        svm_analyzer.load_data(args.test_type)
    else:
        svm_analyzer.load_data()
    
    if args.evaluation_method == EVAL_TRAIN_ACC_LINEAR and args.test_type != STR_TEST_TYPE_ONE_VS_ALL:
        svm_analyzer.set_training_accuracies(args.back_svm_train_acc,
                                             args.front_svm_train_acc,
                                             args.left_svm_train_acc,
                                             args.right_svm_train_acc)
        svm_analyzer.train_acc_linear_decision_function()
        test_accuracy = svm_analyzer.aggregate_test_accuracy()
        print "Aggregate test accuracy: " + str(test_accuracy)
    
    elif args.test_type == STR_TEST_TYPE_ONE_VS_ONE:
        svm_analyzer.generate_svm_results(args.test_type)   
        svm_analyzer.svm_wise_test_accuracies(args.test_type)
    else:
        svm_analyzer.generate_svm_results()   
        svm_analyzer.svm_wise_test_accuracies()
    
