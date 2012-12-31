'''
Created on Nov 30, 2012

@author: mandar
'''

from glimpse.glab import *
from glimpse.util import svm
import os

class SVM(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''       

        self.training_accuracy = None
        self.testing_accuracy = None
        self.testing_decision_values = None
        self.image_to_decision_value = {}
        self.experiment = SetExperiment()
        
    @classmethod
    def set_data(self, training_images_path, testing_images_path=None):
        
        self.class_name = os.path.basename(training_images_path)

        print "initializing the " + self.class_name + " SVM ..."        
        
        self.training_images_path = training_images_path
        self.testing_images_path = testing_images_path
        
        if testing_images_path is None:
            self.experiment.SetCorpus(self.training_images_path, balance=True)
        else:
            self.experiment.SetTrainTestSplitFromDirs(self.training_images_path, self.testing_images_path)
    
    @classmethod
    def configure_svm(self, num_of_prototypes):
        
        print "configuring the " + self.class_name + " SVM ..."
        self.num_of_prototypes = num_of_prototypes
        self.experiment.ImprintS2Prototypes(self.num_of_prototypes)
        
    @classmethod
    def train(self):
        
        print "training the " + self.class_name + " SVM ..."
        self.training_accuracy = self.experiment.TrainSvm()
        print "training accuracy: " + str(self.training_accuracy)
    
    @classmethod
    def test(self):
        
        print "testing the " + self.class_name + " SVM ..."
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