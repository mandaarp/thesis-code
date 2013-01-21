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
        SetModelClass('ml')
        params = GetParams()
        params.image_resize_method = 'scale short edge'
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

    def rbf_train(self):
        
        import sklearn.metrics
        import sklearn.pipeline
        import sklearn.preprocessing
        import sklearn.svm
        
        """Construct an SVM classifier from the set of training images.

        :returns: Training accuracy.
        :rtype: float
    
        """
        if self.experiment.train_features == None:
            self.experiment.ComputeFeatures()
        # Prepare the data
        train_features, train_labels = svm.PrepareFeatures(self.experiment.train_features)
        # Create the SVM classifier with feature scaling.
        self.experiment.classifier = svm.Pipeline([ ('scaler', sklearn.preprocessing.Scaler()),
            ('svm', sklearn.svm.NuSVC(gamma=0.00001))])
        self.experiment.classifier.fit(train_features, train_labels)
        # Evaluate the classifier
        decision_values = self.experiment.classifier.decision_function(train_features)
        predicted_labels = self.experiment.classifier.predict(train_features)
        accuracy = sklearn.metrics.zero_one_score(train_labels, predicted_labels)
        fpr, tpr, thresholds = sklearn.metrics.roc_curve(train_labels, predicted_labels)
        auc = sklearn.metrics.auc(fpr, tpr)
        self.experiment.train_results = dict(decision_values = decision_values,
            predicted_labels = predicted_labels, accuracy = accuracy, auc = auc)
        return self.experiment.train_results['accuracy']
    
    def rbf_crossvalidate_train(self):
        
        import sklearn.metrics
        import sklearn.pipeline
        import sklearn.preprocessing
        import sklearn.svm
        
        """Test a learned SVM classifier.

        The classifier is applied to all images using 10-by-10-way cross-validation.
    
        :returns: Cross-validation accuracy
        :rtype: float
    
        """
        if self.experiment.train_features == None:
            self.experiment.ComputeFeatures()
        features, labels = svm.PrepareFeatures(self.experiment.GetFeatures())
        # Create the SVM classifier with feature scaling.
        classifier = svm.Pipeline([ ('scaler', sklearn.preprocessing.Scaler()),
            ('svm', sklearn.svm.NuSVC(nu=0.5, gamma=0.00001))])
        scores = sklearn.cross_validation.cross_val_score(classifier, features,
            labels, cv = 10, n_jobs = -1)
        test_accuracy = scores.mean()
        self.experiment.train_results = None
        self.experiment.test_results = dict(accuracy = test_accuracy)
        self.experiment.cross_validated = True
        return test_accuracy
              
    def train(self):
        
        print "SVM: training the " + self.class_name + " SVM ..."
        self.training_accuracy = self.experiment.TrainSvm()
        #self.training_accuracy = self.rbf_train()       
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
