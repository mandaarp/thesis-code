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
        
        self.svm_person_back_vs_front = None
        self.svm_person_back_vs_left = None
        self.svm_person_back_vs_right = None
        
        self.svm_person_front_vs_left = None
        self.svm_person_front_vs_right = None
        
        self.svm_person_left_vs_right = None
        
        self.image_to_class = {}
        self.total_test_images = 0
        self.positives = 0
        self.negatives = 0
                
        self.decision_values_file_data = []
        
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

    def generate_svm(self):
        
        print "DirectionEstimator: generating SVMs - one for each direction ..."        

        self.svm_person_back_vs_front = svm.SVM()
        self.svm_person_back_vs_front.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_BACK_VS_FRONT), 
                                               os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_BACK_VS_FRONT))

        self.svm_person_back_vs_left = svm.SVM()
        self.svm_person_back_vs_left.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_BACK_VS_LEFT),
                                              os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_BACK_VS_LEFT))
    
        self.svm_person_back_vs_right = svm.SVM()
        self.svm_person_back_vs_right.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_BACK_VS_RIGHT),
                                               os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_BACK_VS_RIGHT))
    
        self.svm_person_front_vs_left = svm.SVM()
        self.svm_person_front_vs_left.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_FRONT_VS_LEFT),
                                               os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_FRONT_VS_LEFT))
        
        self.svm_person_front_vs_right = svm.SVM()
        self.svm_person_front_vs_right.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_FRONT_VS_RIGHT),
                                                os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_FRONT_VS_RIGHT))
        
        self.svm_person_left_vs_right = svm.SVM()
        self.svm_person_left_vs_right.set_data(os.path.join(self.training_images_path, value.STR_PEDESTRIAN_LEFT_VS_RIGHT),
                                               os.path.join(self.testing_images_path, value.STR_PEDESTRIAN_LEFT_VS_RIGHT))
         
    def imprint_s2_prototypes(self, proto_gen_method, num_of_prototypes):
        
        print "DirectionEstimator: imprinting " + str(num_of_prototypes) + " S2 prototypes for each SVM using " + proto_gen_method + " ..."
        self.svm_person_back_vs_front.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_back_vs_left.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_back_vs_right.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_front_vs_left.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_front_vs_right.configure_svm(proto_gen_method, num_of_prototypes)
        self.svm_person_left_vs_right.configure_svm(proto_gen_method, num_of_prototypes)
        
    def train(self):
        
        print "DirectionEstimator: training each SVM ..."
        self.svm_person_back_vs_front.train()
        self.svm_person_back_vs_left.train()
        self.svm_person_back_vs_right.train()
        self.svm_person_front_vs_left.train()
        self.svm_person_front_vs_right.train()
        self.svm_person_left_vs_right.train()
    
    def test(self):
        
        print "DirectionEstimator: testing each SVM ..."
        self.svm_person_back_vs_front.test()
        self.svm_person_back_vs_left.test()
        self.svm_person_back_vs_right.test()
        self.svm_person_front_vs_left.test()
        self.svm_person_front_vs_right.test()
        self.svm_person_left_vs_right.test()
    
    def print_decision_values(self):
        
        print "DirectionEstimator: printing image-to-decision-values ..."
        print self.svm_person_back_vs_front.image_to_decision_value
        print self.svm_person_back_vs_left.image_to_decision_value
        print self.svm_person_back_vs_right.image_to_decision_value
        print self.svm_person_front_vs_left.image_to_decision_value
        print self.svm_person_front_vs_right.image_to_decision_value
        print self.svm_person_left_vs_right.image_to_decision_value
        
    def dump_experiments(self, file_path):
                
        print "DirectionEstimator: dumping experiments at " + file_path + " ..."
        self.svm_person_back_vs_front.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_BACK_VS_FRONT))
        self.svm_person_back_vs_left.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_BACK_VS_LEFT))
        self.svm_person_back_vs_right.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_BACK_VS_RIGHT))
        self.svm_person_front_vs_left.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_FRONT_VS_LEFT))
        self.svm_person_front_vs_right.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_FRONT_VS_RIGHT))
        self.svm_person_left_vs_right.experiment.Store(os.path.join(file_path, value.STR_PEDESTRIAN_LEFT_VS_RIGHT))

    def get_winner_class_argmax(self, class_back_count, class_front_count, class_left_count, class_right_count):
        
        max_count = class_back_count
        winner_class = value.STR_PEDESTRIAN_BACK
        
        if max_count < class_front_count:
            max_count = class_front_count
            winner_class = value.STR_PEDESTRIAN_FRONT
        elif max_count < class_left_count:
            max_count = class_left_count
            winner_class = value.STR_PEDESTRIAN_LEFT
        elif max_count < class_right_count:
            max_count = class_right_count
            winner_class = value.STR_PEDESTRIAN_RIGHT
        
        return winner_class
            
    def pairwise_classification(self, key):
        
        class_back_count = 0
        class_front_count = 0
        class_left_count = 0
        class_right_count = 0
        
        if self.svm_person_back_vs_front.image_to_decision_value[key] >= 0.0:
            class_back_count = class_back_count + 1
        else:
            class_front_count = class_front_count + 1
            
        if self.svm_person_back_vs_left.image_to_decision_value[key] >= 0.0:
            class_back_count = class_back_count + 1
        else:
            class_left_count = class_left_count + 1
                
        if self.svm_person_back_vs_right.image_to_decision_value[key] >= 0.0:
            class_back_count = class_back_count + 1
        else:
            class_right_count = class_right_count + 1
            
        if self.svm_person_front_vs_left.image_to_decision_value[key] >= 0.0:
            class_front_count = class_front_count + 1
        else:
            class_left_count = class_left_count + 1
        
        if self.svm_person_front_vs_right.image_to_decision_value[key] >= 0.0:
            class_front_count = class_front_count + 1
        else:
            class_right_count = class_right_count + 1
        
        if self.svm_person_left_vs_right.image_to_decision_value[key] >= 0.0:
            class_left_count = class_left_count + 1
        else:
            class_right_count = class_right_count + 1
        
        final_class = self.get_winner_class_argmax(class_back_count,
                                                   class_front_count,
                                                   class_left_count,
                                                   class_right_count)
        
        self.decision_values_file_data.append(str(key) + "," + 
                                              str(self.svm_person_back_vs_front.image_to_decision_value[key]) + "," +
                                              str(self.svm_person_back_vs_left.image_to_decision_value[key]) + "," +
                                              str(self.svm_person_back_vs_right.image_to_decision_value[key]) + "," +
                                              str(self.svm_person_front_vs_left.image_to_decision_value[key]) + "," +
                                              str(self.svm_person_front_vs_right.image_to_decision_value[key]) + "," +
                                              str(self.svm_person_left_vs_right.image_to_decision_value[key]) + "," +
                                              str(class_back_count) + "," +
                                              str(class_front_count) + "," +
                                              str(class_left_count) + "," +
                                              str(class_right_count) + "," +
                                              str(final_class)
                                              )
        
        return final_class
        
    def decision_function_pairwise_classification(self):
        
        self.decision_values_file_data.append("Actual class," +
                                              "pedestrian-back-vs-front," +
                                              "pedestrian-back-vs-left," +
                                              "pedestrian-back-vs-right," +
                                              "pedestrian-front-vs-left," +
                                              "pedestrian-front-vs-right," +
                                              "pedestrian-left-vs-right," +
                                              "class-pedestrian-back-count," +
                                              "class-pedestrian-front-count," +
                                              "class-pedestrian-left-count," +
                                              "class-pedestrian-right-count," +
                                              "winner")
        
        for image in self.svm_person_back_vs_front.image_to_decision_value.iterkeys():
            self.image_to_class[image] = self.pairwise_classification(image)  

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
        
        print "back-as-back  : " + str(self.back_as_back)
        print "back-as-front : " + str(self.back_as_front)
        print "back-as-left  : " + str(self.back_as_left)
        print "back-as-right : " + str(self.back_as_right)
        print "\n"
        print "front-as-back : " + str(self.front_as_back)
        print "front-as-front: " + str(self.front_as_front)
        print "front-as-left : " + str(self.front_as_left)
        print "front-as-right: " + str(self.front_as_right)
        print "\n"
        print "left-as-back  : " + str(self.left_as_back)
        print "left-as-front : " + str(self.back_as_front)
        print "left-as-left  : " + str(self.left_as_left)
        print "left-as-right : " + str(self.left_as_right)
        print "\n"
        print "right-as-back : " + str(self.right_as_back)
        print "right-as-front: " + str(self.right_as_front)
        print "right-as-left : " + str(self.right_as_left)
        print "right-as-right: " + str(self.right_as_right)
        print "\n"

    def dump_decision_values(self):
        
        decision_values_file = open(value.STR_DECISION_VALUES_FILE, "w")
        
        for line in range(len(self.decision_values_file_data)):
            decision_values_file.write(self.decision_values_file_data[line] + "\n")
            
        decision_values_file.close()