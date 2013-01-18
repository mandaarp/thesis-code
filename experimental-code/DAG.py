'''
Created on Jan 17, 2013

@author: mandar
'''

import argparse

STR_PEDESTRIAN_BACK = "pedestrian-back"
STR_PEDESTRIAN_FRONT = "pedestrian-front"
STR_PEDESTRIAN_LEFT = "pedestrian-left"
STR_PEDESTRIAN_RIGHT = "pedestrian-right"

class DAG(object):
    '''
    classdocs
    '''


    def __init__(self, decision_values_file):
        '''
        Constructor
        '''
        self.decision_values_file = decision_values_file
        
        self.back_vs_front_image_to_value = {}
        self.back_vs_left_image_to_value = {}
        self.back_vs_right_image_to_value = {}
        self.front_vs_left_image_to_value = {}
        self.front_vs_right_image_to_value = {}
        self.left_vs_right_image_to_value = {}
        
        self.back_vs_front_DAG_results = {}
        
    def parse_decision_values(self):
        
        file = open(self.decision_values_file, "r")
        file_data = file.readlines()
        file.close()
        
        for line in file_data[1:]:
            csv_line = line.split(',')[0:7]
            
            self.back_vs_front_image_to_value[csv_line[0]] = float(csv_line[1])
            self.back_vs_left_image_to_value[csv_line[0]] = float(csv_line[2])
            self.back_vs_right_image_to_value[csv_line[0]] = float(csv_line[3])
            self.front_vs_left_image_to_value[csv_line[0]] = float(csv_line[4])
            self.front_vs_right_image_to_value[csv_line[0]] = float(csv_line[5])
            self.left_vs_right_image_to_value[csv_line[0]] = float(csv_line[6])
    
    def DAG_back_vs_front(self):
        
        for line in self.back_vs_front_image_to_value:
            if self.back_vs_front_image_to_value[line] > 0:
                if self.left_vs_right_image_to_value[line] > 0:
                    if self.back_vs_left_image_to_value[line] > 0:
                        self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_BACK
                    else:
                        self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_LEFT
                elif self.back_vs_right_image_to_value[line] > 0:
                    if self.back_vs_right_image_to_value[line] > 0:
                        self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_BACK
                    else:
                        self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_RIGHT
            else:
                if self.left_vs_right_image_to_value[line] > 0:
                    if self.front_vs_left_image_to_value[line] > 0:
                        self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_FRONT
                    else:
                        self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_LEFT
                elif self.front_vs_right_image_to_value[line] > 0:
                    self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_FRONT
                else:
                    self.back_vs_front_DAG_results[line] = STR_PEDESTRIAN_RIGHT
    
    def get_testing_accuracy(self):
        
        true_positives = 0
        
        for line in self.back_vs_front_DAG_results:
            if self.back_vs_front_DAG_results[line] in line:
                true_positives = true_positives + 1
        
        accuracy = float(true_positives) / float(len(self.back_vs_front_DAG_results))
        print "accuracy in fraction: " + str(accuracy)
        print "accuracy: " + str(float(accuracy)*100.0) + " %"

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='DAG evaulation')
    parser.add_argument("-f", "--decision-values-file", required=True, type=str, action="store",
                        dest='decision_values_file', help='path to decision_values.csv file')
    args = parser.parse_args()
    
    dag = DAG(args.decision_values_file)
    
    dag.parse_decision_values()
    
    dag.DAG_back_vs_front()
    
    dag.get_testing_accuracy()