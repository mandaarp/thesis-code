'''
Created on Nov 30, 2012

@author: mandar
'''

from glimpse.glab import *
from glimpse.util import svm
import os
import Constants as value

class SVM(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''       
        self.training_images_path = None
        self.testing_images_path = None
        self.class_name = None
        self.training_accuracy = None
        self.testing_accuracy = None
        self.testing_decision_values = None
        self.image_to_decision_value = {}
        self.experiment = None
        
    def set_data(self, training_images_path, testing_images_path=None):
        
        print "SVM: training path: " + training_images_path
        self.class_name = os.path.basename(training_images_path)
        print "SVM: class name: " + os.path.basename(training_images_path)
        
        print "SVM: initializing the " + self.class_name + " SVM ..."        
        
        self.training_images_path = training_images_path
        self.testing_images_path = testing_images_path
        self.experiment = SetExperiment()
        
        if testing_images_path is None:
            self.experiment.SetCorpus(self.training_images_path)
        else:
            self.experiment.SetTrainTestSplitFromDirs(self.training_images_path, self.testing_images_path)
    
    def configure_svm(self, proto_gen_method, num_of_prototypes):
        
        print "SVM: configuring the " + self.class_name + " SVM ..."
        self.num_of_prototypes = num_of_prototypes
        
        if value.STR_IMPRINT_S2_PROTOTYPES == proto_gen_method:
            self.experiment.ImprintS2Prototypes(self.num_of_prototypes)
            
        if value.STR_MAKE_HISTOGRAM_RANDOM_S2_PROTOTYPES == proto_gen_method:
            self.experiment.MakeHistogramRandomS2Prototypes(self.num_of_prototypes)
        
        if value.STR_MAKE_NORMAL_RANDOM_S2_PROTOTYPES == proto_gen_method:
            self.experiment.MakeNormalRandomS2Prototypes(self.num_of_prototypes)
        
        if value.STR_MAKE_SHUFFLED_RANDOM_S2_PROTOTYPES == proto_gen_method:
            self.experiment.MakeShuffledRandomS2Prototypes(self.num_of_prototypes)
        
        if value.STR_MAKE_UNIFORM_RANDOM_S2_PROTOTYPES == proto_gen_method:
            self.experiment.MakeUniformRandomS2Prototypes(self.num_of_prototypes)
        
    def train(self):
        
        print "SVM: training the " + self.class_name + " SVM ..."
        self.training_accuracy = self.experiment.TrainSvm()
        print "SVM: training accuracy: " + str(self.training_accuracy)
    
    def test(self):
        
        print "SVM: testing the " + self.class_name + " SVM ..."
        test_features, test_labels = svm.PrepareFeatures(self.experiment.test_features)
        self.testing_decision_values = self.experiment.classifier.decision_function(test_features)
        
        self.testing_decision_values = self.testing_decision_values.tolist()
        
        if len(self.experiment.test_images[1]) > 0:
            for index in range(len(self.testing_decision_values)):
                self.image_to_decision_value[os.path.basename(self.experiment.test_images[1][index])] = self.testing_decision_values[index][0]
        elif len(self.experiment.test_images[0]) > 0:
            for index in range(len(self.testing_decision_values)):
                self.image_to_decision_value[os.path.basename(self.experiment.test_images[0][index])] = self.testing_decision_values[index][0]
        else:
            print "ERROR: invalid experiment.test_images in " + self.class_name
            return
            
        return self.image_to_decision_value