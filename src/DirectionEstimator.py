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
        
        self.back_as_back = 0
        self.back_as_front = 0
        self.back_as_left = 0
        self.back_as_right = 0
        
        self.front_as_back = 0
        self.front_as_front = 0
        self.front_as_left = 0
        self.front_as_right = 0
        
        self.left_as_back = 0
        self.left_as_front = 0
        self.left_as_left = 0
        self.left_as_right = 0
        
        self.right_as_back = 0
        self.right_as_front = 0
        self.right_as_left = 0
        self.right_as_right = 0
        
        self.decision_values_file_data = []
        
    def generate_svm(self):
        
        if self.debug is True:
            print "DirectionEstimator: generating SVMs - debug mode ..."
            
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
        
        print "DirectionEstimator: generating SVMs - one for each direction ..."        

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
 
    def imprint_s2_prototypes(self, proto_gen_method, num_of_prototypes):
        
        if self.debug is True:
            
            print "DirectionEstimator: imprinting " + str(num_of_prototypes) + " S2 prototypes for each SVM using " + proto_gen_method + " - debug mode ..."            
            self.svm_person_back.configure_svm(proto_gen_method, num_of_prototypes)
            self.svm_person_forward.configure_svm(proto_gen_method, num_of_prototypes)
            
            return
        
        print "DirectionEstimator: imprinting " + str(num_of_prototypes) + " S2 prototypes for each SVM using " + proto_gen_method + " ..."
        self.svm_person_back.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_forward.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_left.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_right.configure_svm(proto_gen_method, num_of_prototypes)
        
    def train(self):
        
        if self.debug is True:
            
            print "DirectionEstimator: training each SVM - debug mode"
            self.svm_person_back.train()
            self.svm_person_forward.train()
            
            return
        
        print "DirectionEstimator: training each SVM ..."
#        self.svm_person_back.train()
        self.svm_person_back.cross_validate()
        
#        self.svm_person_forward.train()
        self.svm_person_forward.cross_validate()
        
#        self.svm_person_left.train()
        self.svm_person_left.cross_validate()
        
#        self.svm_person_right.train()
        self.svm_person_right.cross_validate()
    
    def test(self):
        
        if self.debug is True:
            
            print "DirectionEstimator: testing each SVM - debug mode ..."
            self.svm_person_back.test()
            self.svm_person_forward.test()
            
            return
        
        print "DirectionEstimator: testing each SVM ..."
        self.svm_person_back.test()
        self.svm_person_forward.test()
        self.svm_person_left.test()
        self.svm_person_right.test()
    
    def print_decision_values(self):
        
        if self.debug is True:
            
            print "DirectionEstimator: printing image-to-decision-values - debug mode ..."
            print self.svm_person_back.image_to_decision_value
            print self.svm_person_forward.image_to_decision_value
            
            return
            
        print "DirectionEstimator: printing image-to-decision-values ..."
        print self.svm_person_back.image_to_decision_value
        print self.svm_person_forward.image_to_decision_value
        print self.svm_person_left.image_to_decision_value
        print self.svm_person_right.image_to_decision_value
        
    def dump_experiments(self, file_path):
        
        if self.debug is True:
            
            print "DirectionEstimator: dumping debug mode experiments at " + file_path + " ..."
            self.svm_person_back.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_BACK))
            self.svm_person_forward.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_FRONT))
            
            return
        
        print "DirectionEstimator: dumping experiments at " + file_path + " ..."
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
        
        self.decision_values_file_data.append(str(key) + "," + str(self.svm_person_back.image_to_decision_value[key]) + "," + 
                                              str(self.svm_person_forward.image_to_decision_value[key]) + "," + 
                                              str(self.svm_person_left.image_to_decision_value[key]) + "," +
                                              str(self.svm_person_right.image_to_decision_value[key]) + "," + 
                                              str(final_class))
        
        return final_class
        
    def decision_function_argmax(self):
        
        self.decision_values_file_data.append("Actual class,pedestrian-back, pedestrian-front, pedestrian-left, pedestrian-right, winner")
        
        for image in self.svm_person_back.image_to_decision_value.iterkeys():
            self.image_to_class[image] = self.argmax(image)  

    def dump_classification(self, file_path):

        print "DirectionEstimator: writing classifications in " + file_path + " ..."        
        classification_file = open(file_path, 'w')
        for key in self.image_to_class.iterkeys():
            classification_file.write(key + "," + self.image_to_class[key] + "\n")
        classification_file.close()

    def predict_test_accuracy(self):
        
        print "DirectionEstimator: predicting test accuracy ..."
        self.total_images = len(self.image_to_class)
        
        for key in self.image_to_class.iterkeys():
            if self.image_to_class[key] in key:
#                print "match found: " + key + " -> " + self.image_to_class[key] + "\n" 
                self.positives = self.positives + 1
            else:
                self.update_confusion_matrix(self.image_to_class[key],key)
                 
        print "DirectionEstimator: self.positives: " + str(self.positives)
        print "DirectionEstimator: self.total_images: " + str(self.total_images)
        
        return (float(self.positives) / float(self.total_images))
    
    def update_confusion_matrix(self, predicted_class, image_path):
        
        if value.STR_PEDESTRIAN_BACK == predicted_class:
            if value.STR_PEDESTRIAN_BACK in image_path:
                self.back_as_back = self.back_as_back + 1
            elif value.STR_PEDESTRIAN_FRONT in image_path:
                self.front_as_back = self.front_as_back + 1
            elif value.STR_PEDESTRIAN_LEFT in image_path:
                self.left_as_back = self.left_as_back + 1
            elif value.STR_PEDESTRIAN_RIGHT in image_path:
                self.right_as_back = self.right_as_back + 1
             
        if value.STR_PEDESTRIAN_FRONT == predicted_class:
            if value.STR_PEDESTRIAN_BACK in image_path:
                self.back_as_front = self.back_as_front + 1
            elif value.STR_PEDESTRIAN_FRONT in image_path:
                self.front_as_front = self.front_as_front + 1
            elif value.STR_PEDESTRIAN_LEFT in image_path:
                self.left_as_front = self.left_as_front + 1
            elif value.STR_PEDESTRIAN_RIGHT in image_path:
                self.right_as_front = self.right_as_front + 1

        if value.STR_PEDESTRIAN_LEFT == predicted_class:
            if value.STR_PEDESTRIAN_BACK in image_path:
                self.back_as_left = self.back_as_left + 1
            elif value.STR_PEDESTRIAN_FRONT in image_path:
                self.front_as_left = self.front_as_left + 1
            elif value.STR_PEDESTRIAN_LEFT in image_path:
                self.left_as_left = self.left_as_left + 1
            elif value.STR_PEDESTRIAN_RIGHT in image_path:
                self.right_as_left = self.right_as_left + 1

        if value.STR_PEDESTRIAN_RIGHT == predicted_class:
            if value.STR_PEDESTRIAN_BACK in image_path:
                self.back_as_right = self.back_as_right + 1
            elif value.STR_PEDESTRIAN_FRONT in image_path:
                self.front_as_right = self.front_as_right + 1
            elif value.STR_PEDESTRIAN_LEFT in image_path:
                self.left_as_right = self.left_as_right + 1
            elif value.STR_PEDESTRIAN_RIGHT in image_path:
                self.right_as_right = self.right_as_right + 1

    def print_confusion_matrix(self):
        
        print " ========== confusion matrix =========="
        print "back-as-front : " + str(self.back_as_front)
        print "back-as-left  : " + str(self.back_as_left)
        print "back-as-right : " + str(self.back_as_right)
        print "\n"
        print "front-as-back : " + str(self.front_as_back)
        print "front-as-left : " + str(self.front_as_left)
        print "front-as-right: " + str(self.front_as_right)
        print "\n"
        print "left-as-back  : " + str(self.left_as_back)
        print "left-as-front : " + str(self.back_as_front)
        print "left-as-right : " + str(self.left_as_right)
        print "\n"
        print "right-as-back : " + str(self.right_as_back)
        print "right-as-front: " + str(self.right_as_front)
        print "right-as-left : " + str(self.right_as_left)
        print "\n"

    def dump_decision_values(self):
        
        decision_values_file = open(value.STR_DECISION_VALUES_FILE, "w")
        
        for line in range(len(self.decision_values_file_data)):
            decision_values_file.write(self.decision_values_file_data[line] + "\n")
            
        decision_values_file.close()