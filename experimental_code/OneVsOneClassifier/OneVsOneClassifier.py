'''
Created on Jan 27, 2013

@author: mandar
'''

import sys,os
source_path = os.path.join(os.environ['HOME'],"thesis-code")
if source_path not in sys.path:
    sys.path.insert(0,source_path)
    
from glimpse.glab import *
import glimpse.util.svm as glimpse_svm
import sklearn.svm as sklearn_svm
import sklearn.preprocessing as sklearn_preprocessing
import sklearn.multiclass as sklearn_multiclass
import sklearn.metrics as sklearn_metrics
import sklearn.cross_validation as sklearn_cross_validation
import src.Constants as values

class OneVsOneClassifier(object):
    
    def __init__(self):
        self.classifer = None
        self.train_path = None
        self.test_path = None
        self.proto_gen_method = None
        self.num_of_prototypes = None
        self.prototype_layer = None
        self.kernel = None
        self.gamma = None
        self.constant = None
        params = GetParams()
        params.image_resize_method = 'scale short edge'
        SetParams(params)
        self.train_features = None
        self.train_labels = None
        self.test_features = None
        self.test_labels = None
        self.train_accuracy = None
        self.cross_validation_accuracy = None
        self.test_accuracy = None
        self.predicted_train_labels = None
        self.predicted_test_labels = None
        self.train_auc = None
        self.test_auc = None
        
        
    def set_corpus(self, train_path, test_path):
        self.train_path = train_path
        self.test_path = test_path
    
    def set_prototype_layer(self, prototype_layer="C2"):
        self.prototype_layer = prototype_layer
        
    def set_prototypes_generation_method(self, proto_gen_method, num_of_prototypes):
        self.proto_gen_method = proto_gen_method
        self.num_of_prototypes = num_of_prototypes
            
    def configure_classifier(self, kernel='rbf', gamma=0.001, constant=1.0):
        self.kernel = kernel
        self.gamma = gamma
        self.constant = constant
    
    def generate_experiment(self):
        self.experiment = SetExperiment()#model=SetModelClass('ml'), layer=SetLayer(self.prototype_layer))
        self.experiment.SetTrainTestSplitFromDirs(self.train_path, self.test_path)
        
    def generate_prototypes(self):
        
        if values.STR_IMPRINT_S2_PROTOTYPES == self.proto_gen_method:
            self.experiment.ImprintS2Prototypes(self.num_of_prototypes)
        elif values.STR_MAKE_HISTOGRAM_RANDOM_S2_PROTOTYPES == self.proto_gen_method:
            self.experiment.MakeHistogramRandomS2Prototypes(self.num_of_prototypes)
        elif values.STR_MAKE_NORMAL_RANDOM_S2_PROTOTYPES == self.proto_gen_method:
            self.experiment.MakeNormalRandomS2Prototypes(self.num_of_prototypes)
        elif values.STR_MAKE_SHUFFLED_RANDOM_S2_PROTOTYPES == self.proto_gen_method:
            self.experiment.MakeShuffledRandomS2Prototypes(self.num_of_prototypes)
        elif values.STR_MAKE_UNIFORM_RANDOM_S2_PROTOTYPES == self.proto_gen_method:
            self.experiment.MakeUniformRandomS2Prototypes(self.num_of_prototypes)
            
    def extract_features(self):
        
        self.experiment.ComputeFeatures()
        self.train_features, self.train_labels = glimpse_svm.PrepareFeatures(self.experiment.train_features)
        self.test_features, self.test_labels = glimpse_svm.PrepareFeatures(self.experiment.test_features)
        
    def generate_classifier(self):
        self.classifer = sklearn_multiclass.OneVsOneClassifier(sklearn_svm.SVC(kernel=self.kernel, 
                                                                       gamma=self.gamma, 
                                                                       C=self.constant))
    
    def cross_validate_classifier(self):
        self.train_classifier()
        self.cross_validation_accuracy = sklearn_cross_validation.cross_val_score(self.classifer,
                                                                       self.train_features,
                                                                       self.train_labels,
                                                                       cv=3,
                                                                       n_jobs=-1).mean()
    
    def train_classifier(self):
        self.classifer.fit(self.train_features, self.train_labels)
        self.predicted_train_labels = self.classifer.predict(self.train_features)
        self.train_accuracy = sklearn_metrics.zero_one_score(self.train_labels, self.predicted_train_labels)
        
    def test_classifier(self):
        self.predicted_test_labels = self.classifer.predict(self.test_features)
        self.test_accuracy = sklearn_metrics.zero_one_score(self.test_labels, self.predicted_test_labels)

    def display_results(self):
        
        print "classifier object              : " + str(self.classifer)
        print "training path                  : " + str(self.train_path)
        print "testing path                   : " + str(self.test_path)
        print "prototype generation method    : " + str(self.proto_gen_method)
        print "number of prototypes           : " + str(self.num_of_prototypes)
        print "prototype layer                : " + str(self.prototype_layer)
        print "kernel                         : " + str(self.kernel)
        print "gamma                          : " + str(self.gamma)
        print "constant C                     : " + str(self.constant)
        print "training accuracy              : " + str(self.train_accuracy)
        print "cross validation accuracy      : " + str(self.cross_validation_accuracy)
        print "testing accuracy               : " + str(self.test_accuracy)
        print "training area under curve      : " + str(self.train_auc)
        print "testing area under curve       : " + str(self.test_auc)

if __name__ == '__main__':
    
    import argparse
    
    parser = argparse.ArgumentParser(description='entry point to OneVsAllClassifier')
    parser.add_argument("-t", "--proto-gen-method", required=True, type=str, action="store",dest='proto_gen_method', help='S2 prototype generation method')
    parser.add_argument("-p","--prototypes", required=True, type=int, action="store",dest='num_of_prototypes', help='number of S2 prototypes to imprint')
    parser.add_argument("-s", "--dataset-prefix", required=True, type=str, action="store", dest='dataset_prefix', help='dataset path prefix')
    parser.add_argument("-l","--layer", required=False, default="C2", type=str, action="store", dest='layer', help='prototype layer')
    parser.add_argument("-g","--gamma", required=False, default=0.01, type=float, action="store", dest='gamma', help='SVM kernel gamma')
    parser.add_argument("-k","--kernel", required=False, default="rbf", type=str, action="store", dest='kernel', help='SVM kernel')
    parser.add_argument("-c","--constant", required=False, default=1.0, type=float, action="store", dest='constant', help='SVM kernel constant')
    
    args = parser.parse_args()
    
    print "initializing ..."
    classifier = OneVsOneClassifier()
    
    print "setting corpus ..."
    classifier.set_corpus(os.path.join(args.dataset_prefix, values.STR_TRAIN), os.path.join(args.dataset_prefix, values.STR_TEST))
    
    print "setting prototype layer ..."
    classifier.set_prototype_layer(args.layer)
    
    print "setting prototype generation method ..."
    classifier.set_prototypes_generation_method(args.proto_gen_method, args.num_of_prototypes)

    print "configuring classifier ..."
    classifier.configure_classifier(args.kernel, args.gamma, args.constant)

    print "generating experiment ..."
    classifier.generate_experiment()

    print "generating prototypes ..."
    classifier.generate_prototypes()
    
    print "extracting features ..."
    classifier.extract_features()
    
    print "generating classifier ..."
    classifier.generate_classifier()
    
    print "training classifier ..."
    classifier.train_classifier()
    
#    print "cross-validating classifier ..."
#    classifier.cross_validate_classifier()
    
    print "testing classifier ..."
    classifier.test_classifier()
    
    print "displaying results ...\n"
    classifier.display_results()
