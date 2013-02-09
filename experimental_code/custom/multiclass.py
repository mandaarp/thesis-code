'''
Created on Feb 8, 2013

@author: mandar
'''
import sys,os
source_path = os.path.join(os.environ['HOME'],"thesis-code")
if source_path not in sys.path:
    sys.path.insert(0,source_path)
    
from experimental_code.one_vs_one import Constants as values
import numpy

class MultiClassOneVsOneVoting(object):

    def __init__(self):
        
        self.decision_values_file_path = None
        self.decision_values_data = None

        self.image_to_decision_value_back_vs_front = {}
        self.image_to_decision_value_back_vs_left = {}
        self.image_to_decision_value_back_vs_right = {}
        self.image_to_decision_value_front_vs_left = {}
        self.image_to_decision_value_front_vs_right = {}
        self.image_to_decision_value_left_vs_right = {}
        
        self.image_to_votes_pedestrian_back = {}
        self.image_to_votes_pedestrian_front = {}
        self.image_to_votes_pedestrian_left = {}
        self.image_to_votes_pedestrian_right = {}
        
        self.image_to_votes_pedestrian_back_confidence = {}
        self.image_to_votes_pedestrian_front_confidence = {}
        self.image_to_votes_pedestrian_left_confidence = {}
        self.image_to_votes_pedestrian_right_confidence = {}
        
        self.image_to_prediction = {}
        
    def set_data(self, decision_values_file_path):
        self.decision_values_file_path = decision_values_file_path
        
    def populate_decision_data(self):
        
        decision_file = open(self.decision_values_file_path, "r")
        self.decision_values_data = decision_file.readlines()
        decision_file.close()
    
        for line in self.decision_values_data[1:]:
            csv_line = line.split(',')
            self.image_to_decision_value_back_vs_front[csv_line[0]] = float(csv_line[1])
            self.image_to_decision_value_back_vs_left[csv_line[0]] = float(csv_line[2])
            self.image_to_decision_value_back_vs_right[csv_line[0]] = float(csv_line[3])
            self.image_to_decision_value_front_vs_left[csv_line[0]] = float(csv_line[4])
            self.image_to_decision_value_front_vs_right[csv_line[0]] = float(csv_line[5])
            self.image_to_decision_value_left_vs_right[csv_line[0]] = float(csv_line[6])
            
            self.image_to_votes_pedestrian_back[csv_line[0]] = float(0.0)
            self.image_to_votes_pedestrian_front[csv_line[0]] = float(0.0)
            self.image_to_votes_pedestrian_left[csv_line[0]] = float(0.0)
            self.image_to_votes_pedestrian_right[csv_line[0]] = float(0.0)
            
            self.image_to_votes_pedestrian_back_confidence[csv_line[0]] = float(0.0)
            self.image_to_votes_pedestrian_front_confidence[csv_line[0]] = float(0.0)
            self.image_to_votes_pedestrian_left_confidence[csv_line[0]] = float(0.0)
            self.image_to_votes_pedestrian_right_confidence[csv_line[0]] = float(0.0)
        
    def determine_votes(self):

        #for each image
        for image in self.image_to_decision_value_back_vs_front:
            #for back-vs-front, if decision_value > 0.0 then
            if 0.0 < self.image_to_decision_value_back_vs_front[image]:
                #increase pedestrian-back vote count
                self.image_to_votes_pedestrian_back[image] = self.image_to_votes_pedestrian_back[image] + 1.0
                #add pedestrian-back confidence value
                self.image_to_votes_pedestrian_back_confidence[image] = self.image_to_votes_pedestrian_back_confidence[image] + abs(self.image_to_decision_value_back_vs_front[image])
            else:
                #increase pedestrian-front vote count
                self.image_to_votes_pedestrian_front[image] = self.image_to_votes_pedestrian_front[image] + 1.0
                #add pedestrian-front confidence value
                self.image_to_votes_pedestrian_front_confidence[image] = self.image_to_votes_pedestrian_front_confidence[image] + abs(self.image_to_decision_value_back_vs_front[image])
            
            #for back-vs-left, if decision_value > 0.0 then
            if 0.0 < self.image_to_decision_value_back_vs_left[image]:
                #increase pedestrian-back vote count
                self.image_to_votes_pedestrian_back[image] = self.image_to_votes_pedestrian_back[image] + 1.0
                #add pedestrian-back confidence value
                self.image_to_votes_pedestrian_back_confidence[image] = self.image_to_votes_pedestrian_back_confidence[image] + abs(self.image_to_decision_value_back_vs_left[image])
            else:
                #increase pedestrian-left vote count
                self.image_to_votes_pedestrian_left[image] = self.image_to_votes_pedestrian_left[image] + 1.0
                #add pedestrian-left confidence value
                self.image_to_votes_pedestrian_left_confidence[image] = self.image_to_votes_pedestrian_left_confidence[image] + abs(self.image_to_decision_value_back_vs_left[image])
            
            #for back-vs-right, if decision_value > 0.0 then
            if 0.0 < self.image_to_decision_value_back_vs_right[image]:
                #increase pedestrian-back vote count
                self.image_to_votes_pedestrian_back[image] = self.image_to_votes_pedestrian_back[image] + 1.0
                #add pedestrian-back confidence value
                self.image_to_votes_pedestrian_back_confidence[image] = self.image_to_votes_pedestrian_back_confidence[image] + abs(self.image_to_decision_value_back_vs_right[image])
            else:
                #increase pedestrian-right vote count
                self.image_to_votes_pedestrian_right[image] = self.image_to_votes_pedestrian_right[image] + 1.0
                #add pedestrian-right confidence value
                self.image_to_votes_pedestrian_right_confidence[image] = self.image_to_votes_pedestrian_right_confidence[image] + abs(self.image_to_decision_value_back_vs_right[image])
            
            #for front-vs-left, if decision_value > 0.0 then
            if 0.0 < self.image_to_decision_value_front_vs_left[image]:
                #increase pedestrian-front vote count
                self.image_to_votes_pedestrian_front[image] = self.image_to_votes_pedestrian_front[image] + 1.0
                #add pedestrian-front confidence value
                self.image_to_votes_pedestrian_front_confidence[image] = self.image_to_votes_pedestrian_front_confidence[image] + abs(self.image_to_decision_value_front_vs_left[image])
            else:
                #increase pedestrian-left vote count
                self.image_to_votes_pedestrian_left[image] = self.image_to_votes_pedestrian_left[image] + 1.0
                #add pedestrian-left confidence value
                self.image_to_votes_pedestrian_left_confidence[image] = self.image_to_votes_pedestrian_left_confidence[image] + abs(self.image_to_decision_value_front_vs_left[image])
            
            #for front-vs-right, if decision_value > 0.0 then
            if 0.0 < self.image_to_decision_value_front_vs_right[image]:
                #increase pedestrian-front vote count
                self.image_to_votes_pedestrian_front[image] = self.image_to_votes_pedestrian_front[image] + 1.0
                #add pedestrian-front confidence value
                self.image_to_votes_pedestrian_front_confidence[image] = self.image_to_votes_pedestrian_front_confidence[image] + abs(self.image_to_decision_value_front_vs_right[image])
            else:
                #increase pedestrian-right vote count
                self.image_to_votes_pedestrian_right[image] = self.image_to_votes_pedestrian_right[image] + 1.0
                #add pedestrian-right confidence value
                self.image_to_votes_pedestrian_right_confidence[image] = self.image_to_votes_pedestrian_right_confidence[image] + abs(self.image_to_decision_value_front_vs_right[image])
            #for left-vs-right, if decision_value > 0.0 then
            if 0.0 < self.image_to_decision_value_left_vs_right[image]:
                #increase pedestrian-left vote count
                self.image_to_votes_pedestrian_left[image] = self.image_to_votes_pedestrian_left[image] + 1.0
                #add pedestrian-left confidence value
                self.image_to_votes_pedestrian_left_confidence[image] = self.image_to_votes_pedestrian_left_confidence[image] + abs(self.image_to_decision_value_left_vs_right[image])
            else:
                #increase pedestrian-right vote count
                self.image_to_votes_pedestrian_right[image] = self.image_to_votes_pedestrian_right[image] + 1.0
                #add pedestrian-right confidence value
                self.image_to_votes_pedestrian_right_confidence[image] = self.image_to_votes_pedestrian_right_confidence[image] + abs(self.image_to_decision_value_left_vs_right[image])
                
    def decide(self):
        
        for image in self.image_to_votes_pedestrian_back_confidence:
            max_value_index = numpy.argmax([self.image_to_votes_pedestrian_back_confidence[image], self.image_to_votes_pedestrian_front_confidence[image], self.image_to_votes_pedestrian_left_confidence[image], self.image_to_votes_pedestrian_right_confidence[image]])
            if max_value_index == 0:
                self.image_to_prediction[image] = values.STR_PEDESTRIAN_BACK
            elif max_value_index == 1:
                self.image_to_prediction[image] = values.STR_PEDESTRIAN_FRONT
            elif max_value_index == 2:
                self.image_to_prediction[image] = values.STR_PEDESTRIAN_LEFT
            elif max_value_index == 3:
                self.image_to_prediction[image] = values.STR_PEDESTRIAN_RIGHT
                
    def calculate_accuracy(self):
        
        positives = 0
        total = len(self.image_to_prediction)
        
        for image in self.image_to_prediction:
            if self.image_to_prediction[image] in image:
                positives = positives + 1
        
        accuracy = float((float(positives)/float(total))* 100.0)
    
        return accuracy

if __name__ == '__main__':
    
    import argparse
        
    parser = argparse.ArgumentParser(description='intelligent multiclass')
    parser.add_argument("-f", "--decision-values-file", required=True, type=str, action="store",dest='decision_values_file', help='decision_values_file')
    args = parser.parse_args()
    
    obj = MultiClassOneVsOneVoting()
    obj.set_data(args.decision_values_file)
    obj.populate_decision_data()
    obj.determine_votes()
    obj.decide()
    print "Accuracy: " + str(obj.calculate_accuracy())
