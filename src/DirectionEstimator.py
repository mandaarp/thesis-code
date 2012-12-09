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

    def __init__(self, training_images_path, testing_images_path, debug=False):
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
        
    def generate_svm(self):
        
        if self.debug is True:
            print "generating SVMs - debug mode ..."
            
            self.svm_person_back = svm.SVM(os.path.join(self.training_images_path, value.STR_PERSON_BACK), 
                                   os.path.join(self.testing_images_path, value.STR_PERSON_BACK))
            
            self.svm_person_forward = svm.SVM(os.path.join(self.training_images_path, value.STR_PERSON_FORWARD),
                                          os.path.join(self.testing_images_path, value.STR_PERSON_FORWARD))
            return
        
        print "generating SVMs - one for each direction ..."        
        self.svm_person_back = svm.SVM(os.path.join(self.training_images_path, value.STR_PERSON_BACK), 
                                   os.path.join(self.testing_images_path, value.STR_PERSON_BACK))
    
        self.svm_person_forward = svm.SVM(os.path.join(self.training_images_path, value.STR_PERSON_FORWARD),
                                          os.path.join(self.testing_images_path, value.STR_PERSON_FORWARD))
        
        self.svm_person_left = svm.SVM(os.path.join(self.training_images_path, value.STR_PERSON_LEFT),
                                       os.path.join(self.testing_images_path, value.STR_PERSON_LEFT))
        
        self.svm_person_right = svm.SVM(os.path.join(self.training_images_path, value.STR_PERSON_RIGHT),
                                        os.path.join(self.testing_images_path, value.STR_PERSON_RIGHT))
 
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
        self.svm_person_right.train
    
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
            self.svm_person_back.experiment.Store(os.path.join(file_path, value.STR_PERSON_BACK))
            self.svm_person_forward.experiment.Store(os.path.join(file_path, value.STR_PERSON_FORWARD))
            
            return
        
        print "dumping experiments at " + file_path + " ..."
        self.svm_person_back.experiment.Store(os.path.join(file_path, value.STR_PERSON_BACK))
        self.svm_person_forward.experiment.Store(os.path.join(file_path, value.STR_PERSON_FORWARD))
        self.svm_person_left.experiment.Store(os.path.join(file_path, value.STR_PERSON_LEFT))
        self.svm_person_right.experiment.Store(os.path.join(file_path, value.STR_PERSON_RIGHT))
    
    def argmax(self, key):
        max_value = self.svm_person_back.image_to_decision_value[key]
        final_class = self.svm_person_back.class_name
        
        if max_value < self.svm_person_forward:
            max_value = self.svm_person_forward.image_to_decision_value[key]
            final_class = self.svm_person_forward.class_name
        
        if max_value < self.svm_person_left:
            max_value = self.svm_person_left.image_to_decision_value[key]
            final_class = self.svm_person_left.class_name
        
        if max_value < self.svm_person_right:
            max_value = self.svm_person_right.image_to_decision_value[key]
            final_class = self.svm_person_right.class_name
        
        return final_class
        
    def decision_function_argmax(self):
        
        pass
            
