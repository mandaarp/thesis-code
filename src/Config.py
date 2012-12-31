'''
Created on Dec 30, 2012

@author: mandar
'''

import os

TRAINING_IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis-images/dataset/train")
ALL_TESTING_IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis-images/dataset/test")
IMAGES_PATH = os.path.join(os.environ['HOME'], "thesis-images/dataset/auto")

DATASET_AUTO = True
NUM_OF_PROTOTYPES = 200