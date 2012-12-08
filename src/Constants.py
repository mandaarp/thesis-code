'''
Created on Nov 30, 2012

@author: mandar
'''
import os

TRAINING_IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis/demo/images/train")
TESTING_IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis/demo/images/test")
ALL_TESTING_IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis/demo/images/test/all")

STR_PERSON_BACK = "person-back"
STR_PERSON_FORWARD = "person-forward"
STR_PERSON_LEFT = "person-left"
STR_PERSON_RIGHT = "person-right"

NUM_OF_PROTOTYPES = 200