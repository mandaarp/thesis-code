'''
Created on Feb 4, 2013

@author: mandar
'''

from PIL import Image as img
from scipy.stats import mode
import glob, os, argparse, numpy


class DatasetInfo(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.image_directory = None
    
    def set_image_directory(self, image_directory):
        self.image_directory = image_directory
        
    def populate_aspect_ratios(self, aspect_ratios):
        
        image_files = glob.glob(os.path.join(self.image_directory, "*.jpg"))
        
        for image in image_files:
            i = img.open(image)
            x,y = i.size
            aspect_ratios.append(float(float(x)/float(y)))
        
        return aspect_ratios

if __name__ == '__main__':
    
    aspect_ratios = []
    di = DatasetInfo()
    
    img_dir = os.path.join(os.environ['HOME'], 'thesis-images/dataset/train/pedestrian-back/back')
    di.set_image_directory(img_dir)
    aspect_ratios = di.populate_aspect_ratios(aspect_ratios)
    
    img_dir = os.path.join(os.environ['HOME'], 'thesis-images/dataset/train/pedestrian-front/front')
    di.set_image_directory(img_dir)
    aspect_ratios = di.populate_aspect_ratios(aspect_ratios)
    
    img_dir = os.path.join(os.environ['HOME'], 'thesis-images/dataset/train/pedestrian-left/left')
    di.set_image_directory(img_dir)
    aspect_ratios = di.populate_aspect_ratios(aspect_ratios)
    
    img_dir = os.path.join(os.environ['HOME'], 'thesis-images/dataset/train/pedestrian-right/right')
    di.set_image_directory(img_dir)
    aspect_ratios = di.populate_aspect_ratios(aspect_ratios)
    
    print "total: " + str(len(aspect_ratios))
    print "mean: " + str(numpy.mean(aspect_ratios))
    print "median: " + str(numpy.median(aspect_ratios))
    print "mode: " + str(mode(aspect_ratios)[0][0])
