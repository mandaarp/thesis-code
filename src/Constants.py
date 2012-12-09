'''
Created on Nov 30, 2012

@author: mandar
'''
import os

TRAINING_IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis/demo/images/person/train")
ALL_TESTING_IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis/demo/images/person/test/all")

STR_BACK = "back"
STR_FORWARD = "forward"
STR_LEFT = "left"
STR_RIGHT = "right"

NUM_OF_PROTOTYPES = 200