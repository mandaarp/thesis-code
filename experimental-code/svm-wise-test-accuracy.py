'''
Created on Jan 19, 2013

@author: mandar
'''
import argparse

STR_PEDESTRIAN_BACK = "pedestrian-back"
STR_PEDESTRIAN_FRONT = "pedestrian-front"
STR_PEDESTRIAN_LEFT = "pedestrian-left"
STR_PEDESTRIAN_RIGHT = "pedestrian-right"

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
        
        self.back_svm_predictions = {}
        self.front_svm_predictions = {}
        self.left_svm_predictions = {}
        self.right_svm_predictions = {}
        
    def load_data(self):
        
        decision_values_file = open(self.decision_values_file, "r")
        self.lines = decision_values_file.readlines()
        decision_values_file.close()
        
        for line in self.lines[1:]:
            csv = line.split(',')
            self.back_svm_image_to_decision_value[csv[0]]=float(csv[1])
            self.front_svm_image_to_decision_value[csv[0]]=float(csv[2])
            self.left_svm_image_to_decision_value[csv[0]]=float(csv[3])
            self.right_svm_image_to_decision_value[csv[0]]=float(csv[4])
        
    def _test_svm(self, image_to_decision_value):
        
        actual_to_predicted = {}
        
        for image in image_to_decision_value:
            if image_to_decision_value[image] > 0:
                actual_to_predicted[image] = 1;
            else:
                actual_to_predicted[image] = -1;
                
        return actual_to_predicted

    def generate_svm_results(self):
        
        self.back_svm_predictions = self._test_svm(self.back_svm_image_to_decision_value)
        self.front_svm_predictions = self._test_svm(self.front_svm_image_to_decision_value)
        self.left_svm_predictions = self._test_svm(self.left_svm_image_to_decision_value)
        self.right_svm_predictions = self._test_svm(self.right_svm_image_to_decision_value)
    
    def _get_test_accuracy(self, svm_predictions, actual_class):
        
        true_predictions = 0
        
        for prediction in svm_predictions:
            if svm_predictions[prediction] == 1 and actual_class in prediction:
                true_predictions = true_predictions + 1
            elif svm_predictions[prediction] == -1 and actual_class not in prediction:
                true_predictions = true_predictions + 1
        
        return float((float(true_predictions) / float(len(svm_predictions)))*100.0)

    def test_accuracies(self):
        
        print "calculating test accuracies ..."
        back_svm_test_accuracy = self._get_test_accuracy(self.back_svm_predictions, STR_PEDESTRIAN_BACK)
        front_svm_test_accuracy = self._get_test_accuracy(self.front_svm_predictions, STR_PEDESTRIAN_FRONT)
        left_svm_test_accuracy = self._get_test_accuracy(self.left_svm_predictions, STR_PEDESTRIAN_LEFT)
        right_svm_test_accuracy = self._get_test_accuracy(self.right_svm_predictions, STR_PEDESTRIAN_RIGHT)
        print "test accuracy calculation completed"
        
        print STR_PEDESTRIAN_BACK + ": " + str(back_svm_test_accuracy) + " %"
        print STR_PEDESTRIAN_FRONT + ": " + str(front_svm_test_accuracy) + " %"
        print STR_PEDESTRIAN_LEFT + ": " + str(left_svm_test_accuracy) + " %"
        print STR_PEDESTRIAN_RIGHT + ": " + str(right_svm_test_accuracy) + " %"
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='entry point to direction estimator')
    parser.add_argument("-f", "--decision-value-file", required=True, type=str, action="store",
                        dest='decision_value_file', help='decision_values.csv file path')
    args = parser.parse_args()
    
    svm_analyzer = SVMAnalysis(args.decision_value_file)
    svm_analyzer.load_data()
    svm_analyzer.generate_svm_results()
    svm_analyzer.test_accuracies()
    
