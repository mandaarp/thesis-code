'''
Created on Nov 30, 2012

@author: mandar
'''

import DirectionEstimator as de
import Constants as value

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

    direction_estimator = de.DirectionEstimator(value.TRAINING_IMAGES_PATH, 
                                                value.ALL_TESTING_IMAGES_PATH,
                                                debug=True)
    
    direction_estimator.generate_svm()
    
    direction_estimator.imprint_s2_prototypes(value.NUM_OF_PROTOTYPES)
    
    direction_estimator.train()
    
    direction_estimator.test()
    
    direction_estimator.print_decision_values()

    direction_estimator.dump_experiments(".")

    direction_estimator.decision_function_argmax()
    
    direction_estimator.dump_classification("classification_result.csv")
    
    test_accuracy = direction_estimator.predict_test_accuracy()
    
    print "\n\ntest accuracy: " + str(test_accuracy * 100.0)