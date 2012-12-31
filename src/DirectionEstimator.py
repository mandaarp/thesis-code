'''
Created on Nov 30, 2012

@author: mandar
'''

import Constants as value
import SVM as svm
import os

class DirectionEstimator(object):
    '''
    classdocs
    '''

    def __init__(self, training_images_path, testing_images_path=None, debug=False):
        '''
        Constructor
        '''
        self.debug = debug
        self.training_images_path = training_images_path
        self.testing_images_path = testing_images_path
        
        self.svm_person_left = None
        self.svm_person_right = None
        self.svm_person_back = None
        self.svm_person_forward = None
        self.image_to_class = {}
        self.total_test_images = 0
        self.positives = 0
        self.negatives = 0
        
    def generate_svm(self):
        
        if self.debug is True:
            print "generating SVMs - debug mode ..."
            
            if self.testing_images_path is None:
                self.svm_person_back = svm.SVM()
                self.svm_person_back.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_BACK))
                
                self.svm_person_forward = svm.SVM()
                self.svm_person_forward.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_FRONT))
            
            else:
                self.svm_person_back = svm.SVM()
                self.svm_person_back.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_BACK), 
                                   os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_BACK))
            
                self.svm_person_forward = svm.SVM()
                self.svm_person_forward.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_FRONT),
                                          os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_FRONT))
            
            return
        
        print "generating SVMs - one for each direction ..."        

        if self.testing_images_path is None:
            
            self.svm_person_back = svm.SVM()
            self.svm_person_back.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_BACK))    
          
            self.svm_person_forward = svm.SVM()
            self.svm_person_forward.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_FRONT))
            
            self.svm_person_left = svm.SVM()
            self.svm_person_left.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_LEFT))
            
            self.svm_person_right = svm.SVM()
            self.svm_person_right.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_RIGHT))
        
        else:
            self.svm_person_back = svm.SVM()
            self.svm_person_back.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_BACK), 
                                   os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_BACK))
    
            self.svm_person_forward = svm.SVM()
            self.svm_person_forward.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_FRONT),
                                          os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_FRONT))
        
            self.svm_person_left = svm.SVM()
            self.svm_person_left.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_LEFT),
                                       os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_LEFT))
        
            self.svm_person_right = svm.SVM()
            self.svm_person_right.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_RIGHT),
                                        os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_RIGHT))
 
    def imprint_s2_prototypes(self, num_of_prototypes):
        
        if self.debug is True:
            
            print "imprinting S2 prototypes for each SVM - debug mode ..."            
            self.svm_person_back.configure_svm(num_of_prototypes)
            self.svm_person_forward.configure_svm(num_of_prototypes)
            
            return
        
        print "imprinting S2 prototypes for each SVM ..."
        self.svm_person_back.configure_svm(num_of_prototypes)
        self.svm_person_forward.configure_svm(num_of_prototypes)
        self.svm_person_left.configure_svm(num_of_prototypes)
        self.svm_person_right.configure_svm(num_of_prototypes)
        
    def train(self):
        
        if self.debug is True:
            
            print "training each SVM - debug mode"
            self.svm_person_back.train()
            self.svm_person_forward.train()
            
            return
        
        print "training each SVM ..."
        self.svm_person_back.train()
        self.svm_person_forward.train()
        self.svm_person_left.train()
        self.svm_person_right.train()
    
    def test(self):
        
        if self.debug is True:
            
            print "testing each SVM - debug mode ..."
            self.svm_person_back.test()
            self.svm_person_forward.test()
            
            return
        
        print "testing each SVM ..."
        self.svm_person_back.test()
        self.svm_person_forward.test()
        self.svm_person_left.test()
        self.svm_person_right.test()
    
    def print_decision_values(self):
        
        if self.debug is True:
            
            print "printing image-to-decision-values - debug mode ..."
            print self.svm_person_back.image_to_decision_value
            print self.svm_person_forward.image_to_decision_value
            
            return
            
        print "printing image-to-decision-values ..."
        print self.svm_person_back.image_to_decision_value
        print self.svm_person_forward.image_to_decision_value
        print self.svm_person_left.image_to_decision_value
        print self.svm_person_right.image_to_decision_value
        
    def dump_experiments(self, file_path):
        
        if self.debug is True:
            
            print "dumping debug mode experiments at " + file_path + " ..."
            self.svm_person_back.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_BACK))
            self.svm_person_forward.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_FRONT))
            
            return
        
        print "dumping experiments at " + file_path + " ..."
        self.svm_person_back.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_BACK))
        self.svm_person_forward.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_FRONT))
        self.svm_person_left.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_LEFT))
        self.svm_person_right.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_RIGHT))
    
    def argmax(self, key):
        
        max_value = self.svm_person_back.image_to_decision_value[key]
        final_class = self.svm_person_back.class_name
        
        if self.debug is True:
            
            if max_value < self.svm_person_forward.image_to_decision_value[key]:
                max_value = self.svm_person_forward.image_to_decision_value[key]
                final_class = self.svm_person_forward.class_name
            
            return final_class
        
        if max_value < self.svm_person_forward.image_to_decision_value[key]:
            max_value = self.svm_person_forward.image_to_decision_value[key]
            final_class = self.svm_person_forward.class_name
        
        if max_value < self.svm_person_left.image_to_decision_value[key]:
            max_value = self.svm_person_left.image_to_decision_value[key]
            final_class = self.svm_person_left.class_name
        
        if max_value < self.svm_person_right.image_to_decision_value[key]:
            max_value = self.svm_person_right.image_to_decision_value[key]
            final_class = self.svm_person_right.class_name
        
        return final_class
        
    def decision_function_argmax(self):
        
               
        for image in self.svm_person_back.image_to_decision_value.iterkeys():
            self.image_to_class[image] = self.argmax(image)  

    def dump_classification(self, file_path):

        print "writing classifications in " + file_path + " ..."        
        classification_file = open(file_path, 'w')
        for key in self.image_to_class.iterkeys():
            classification_file.write(key + "," + self.image_to_class[key] + "\n")
        classification_file.close()

    def predict_test_accuracy(self):
        
        print "predicting test accuracy ..."
        self.total_images = len(self.image_to_class)
        
        for key in self.image_to_class.iterkeys():
            if self.image_to_class[key] in key:
                print "match found: " + key + " -> " + self.image_to_class[key] + "\n" 
                self.positives = self.positives + 1
        print "self.positives: " + str(self.positives)
        print "self.total_images: " + str(self.total_images)
        
        return (float(self.positives) / float(self.total_images))