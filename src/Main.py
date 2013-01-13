'''
Created on Nov 30, 2012

@author: mandar
'''

import DirectionEstimator as de
import Constants as value
import Config as config
import argparse
import os

if __name__ == '__main__':
    
#    svm_back = SVM(value.TRAIN_PERSON_BACK, value.TEST_PERSON_BACK)
#    
#    svm_back.configure_svm(value.NUM_OF_PROTOTYPES)
#    
#    svm_back.train()
#    
#    decision_values = svm_back.test()
#    
#    print decision_values
    
    
    parser = argparse.ArgumentParser(description='entry point to direction estimator')
    parser.add_argument("-t", "--proto-gen-method", required=True, type=str, action="store",dest='proto_gen_method', help='S2 prototype generation method')
    parser.add_argument("-p","--prototypes", required=True, type=int, action="store",dest='num_of_prototypes', help='number of S2 prototypes to imprint')
    parser.add_argument("-s", "--dataset-prefix", required=True, type=str, action="store", dest='dataset_prefix', help='dataset path prefix')
    parser.add_argument("-d","--debug", action="store_true", dest='debug', help='debug mode execution')
    args = parser.parse_args()
    
    print "========== Experiment setup =========="
    print "num_of_prototypes: " + str(args.num_of_prototypes)
    print "debug mode: " + str(args.debug)
    print "dataset_prefix: " + args.dataset_prefix
    print "prototype generation method: " + args.proto_gen_method
    
    print "\n\n"
    
#    direction_estimator = de.DirectionEstimator(config.TRAINING_IMAGES_PATH, 
#                                                config.ALL_TESTING_IMAGES_PATH,
#                                                debug=args.debug)

    direction_estimator = de.DirectionEstimator(os.path.join(args.dataset_prefix, value.STR_TRAIN),
                                                os.path.join(args.dataset_prefix, value.STR_TEST),
                                                debug=args.debug)        
    direction_estimator.generate_svm()
    
    direction_estimator.imprint_s2_prototypes(args.proto_gen_method, args.num_of_prototypes)
    
    direction_estimator.train()
    
    direction_estimator.test()
    
#    direction_estimator.dump_experiments(".")

    direction_estimator.decision_function_argmax()
    
    direction_estimator.dump_classification("classification_result.csv")
    
    direction_estimator.dump_decision_values()
    
    test_accuracy = direction_estimator.predict_test_accuracy()
    
    direction_estimator.print_confusion_matrix()

    print "\n Test Accuracy in fraction: " + str(test_accuracy)
    print "\n\ntest accuracy: " + str(test_accuracy * 100.0)
