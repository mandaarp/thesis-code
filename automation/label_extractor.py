'''
Created on Mar 1, 2013

@author: mandar
'''
from sklearn import metrics
import pylab as pl

class One_vs_All(object):
    
    def __init__(self, info_prefix):
        
        self.info_prefix = info_prefix
        self.decision_values_file_lines = None
        
        self.svm_back_image_to_value = {}
        self.svm_front_image_to_value = {}
        self.svm_left_image_to_value = {}
        self.svm_right_image_to_value = {}
        
    def set_label_data(self, decision_values_file):
        
        f = open(decision_values_file, 'r')
        self.decision_values_file_lines = f.readlines()
        f.close()
        
    def populate_decision_values(self):
        
        for line in self.decision_values_file_lines[1:]:
            
            csv = line.split(",")
            self.svm_back_image_to_value[csv[0]] = csv[1]
            self.svm_front_image_to_value[csv[0]] = csv[2]
            self.svm_left_image_to_value[csv[0]] = csv[3]
            self.svm_right_image_to_value[csv[0]] = csv[4]
    
    def generate_roc_auc_data(self, image_to_decision_value, roc_curve_file, label):

        actual_labels = []
        predicted_labels = []
        
        for image in image_to_decision_value:
            
            if label in image:
                actual_labels.append(1)
            else:
                actual_labels.append(-1)
            
            if float(image_to_decision_value[image]) > 0:
                predicted_labels.append(1)
            else:
                predicted_labels.append(-1)
        
        fpr, tpr, thresholds = metrics.roc_curve(actual_labels, predicted_labels)
                
        auc = metrics.auc(fpr, tpr)
        pl.clf()
        pl.plot(fpr, tpr, label="ROC curve (area = %0.2f)" % auc)
        pl.plot([0,1], [0,1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic curve for ' + label)
        pl.legend(loc="lower right")
        pl.savefig(self.info_prefix + "_" + roc_curve_file)
            
    def roc_auc(self):
        
        self.generate_roc_auc_data(self.svm_back_image_to_value, "back_roc_auc.png", "pedestrian-back")
        self.generate_roc_auc_data(self.svm_front_image_to_value, "front_roc_auc.png", "pedestrian-front")
        self.generate_roc_auc_data(self.svm_left_image_to_value, "left_roc_auc.png", "pedestrian-left")
        self.generate_roc_auc_data(self.svm_right_image_to_value, "right_roc_auc.png", "pedestrian-right")

class One_vs_One(object):
    
    def __init__(self, info_prefix):
        
        self.info_prefix = info_prefix
        self.decision_values_file_lines = None
        
        self.svm_back_vs_front_image_to_value = {}
        self.svm_back_vs_left_image_to_value = {}
        self.svm_back_vs_right_image_to_value = {}
        self.svm_front_vs_left_image_to_value = {}
        self.svm_front_vs_right_image_to_value = {}
        self.svm_left_vs_right_image_to_value = {}
                
    def set_label_data(self, decision_values_file):
        
        f = open(decision_values_file, 'r')
        self.decision_values_file_lines = f.readlines()
        f.close()
        
    def populate_decision_values(self):
        
        for line in self.decision_values_file_lines[1:]:
            
            csv = line.split(",")
            self.svm_back_vs_front_image_to_value[csv[0]] = csv[1]
            self.svm_back_vs_left_image_to_value[csv[0]] = csv[2]
            self.svm_back_vs_right_image_to_value[csv[0]] = csv[3]
            self.svm_front_vs_left_image_to_value[csv[0]] = csv[4]
            self.svm_front_vs_right_image_to_value[csv[0]] = csv[5]
            self.svm_left_vs_right_image_to_value[csv[0]] = csv[6]
    
    def a_generate_roc_auc_data(self, image_to_decision_value, roc_curve_file, pos_label, neg_label):

        actual_pos_labels = []
        actual_neg_labels = []
        predicted_pos_labels = []
        predicted_neg_labels = []
        
        for image in image_to_decision_value:
            
            if pos_label in image and float(image_to_decision_value[image]) > 0:
                actual_pos_labels.append(1)
                actual_neg_labels.append(-1)
                predicted_pos_labels.append(1)
                predicted_neg_labels.append(-1)
            elif neg_label in image:
                actual_neg_labels.append(1)
                actual_pos_labels.append(-1)
                predicted_neg_labels.append(1)
                predicted_pos_labels.append(-1)

#            if neg_label in image:
#                actual_neg_labels.append(1)
#            elif pos_label in image:
#                actual_neg_labels.append(-1)
                            
#            if pos_label in image and float(image_to_decision_value[image]) > 0:
#                predicted_pos_labels.append(1)
#                predicted_neg_labels.append(-1)
#            else:                
#                predicted_neg_labels.append(1)
#                predicted_pos_labels.append(-1)
        
        pos_fpr, pos_tpr, pos_thresholds = metrics.roc_curve(actual_pos_labels, predicted_pos_labels)
                
        pos_auc = metrics.auc(pos_fpr, pos_tpr)
        pl.clf()
        pl.plot(pos_fpr, pos_tpr, label="ROC curve (area = %0.2f)" % pos_auc)
        pl.plot([0,1], [0,1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic curve for ' + pos_label)
        pl.legend(loc="lower right")
        pl.savefig("_".join([self.info_prefix, pos_label, roc_curve_file]))
        
        neg_fpr, neg_tpr, neg_thresholds = metrics.roc_curve(actual_neg_labels, predicted_neg_labels)
                
        neg_auc = metrics.auc(neg_fpr, neg_tpr)
        pl.clf()
        pl.plot(pos_fpr, pos_tpr, label="ROC curve (area = %0.2f)" % neg_auc)
        pl.plot([0,1], [0,1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic curve for ' + pos_label)
        pl.legend(loc="lower right")
        
        pl.savefig("_".join([self.info_prefix, neg_label, roc_curve_file]))
            
    def generate_roc_auc_data(self, image_to_decision_value, roc_curve_file, pos_label, neg_label):
        
        actual_labels = []
        predicted_labels = []
        
        for image in image_to_decision_value:
            
            if pos_label in image:
                actual_labels.append(1)
                if float(image_to_decision_value[image]) > 0:
                    predicted_labels.append(1)
                else:
                    predicted_labels.append(-1)
            
            if neg_label in image:
                actual_labels.append(-1)
                if float(image_to_decision_value[image]) < 0:
                    predicted_labels.append(-1)
                else:
                    predicted_labels.append(1)
        
        fpr, tpr, thresholds = metrics.roc_curve(actual_labels, predicted_labels)
                
        auc = metrics.auc(fpr, tpr)
        pl.clf()
        pl.plot(fpr, tpr, label="ROC curve (area = %0.2f)" % auc)
        pl.plot([0,1], [0,1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic curve for ' + pos_label + "_" + neg_label)
        pl.legend(loc="lower right")
        pl.savefig(self.info_prefix + "_" + pos_label + "_" + neg_label + "_" + roc_curve_file)
        
    def roc_auc(self):
        
        self.generate_roc_auc_data(self.svm_back_vs_front_image_to_value, "roc_auc.png", "pedestrian-back", "pedestrian-front")
        self.generate_roc_auc_data(self.svm_back_vs_left_image_to_value, "roc_auc.png", "pedestrian-back", "pedestrian-left")
        self.generate_roc_auc_data(self.svm_back_vs_right_image_to_value, "roc_auc.png", "pedestrian-back", "pedestrian-right")
        self.generate_roc_auc_data(self.svm_front_vs_left_image_to_value, "roc_auc.png", "pedestrian-front", "pedestrian-left")
        self.generate_roc_auc_data(self.svm_front_vs_right_image_to_value, "roc_auc.png", "pedestrian-front", "pedestrian-right")
        self.generate_roc_auc_data(self.svm_left_vs_right_image_to_value, "roc_auc.png", "pedestrian-left", "pedestrian-right")
        
        
if __name__ == '__main__':
    
    import argparse
    
    parser = argparse.ArgumentParser(description='svm-wise label extractor')
    parser.add_argument("-f", "--decision-values-file", required=True, type=str, action="store",
                        dest='decision_values_file', help='decision values file path')
    parser.add_argument("-m", "--method", required=True, type=str, action="store", 
                        dest='method', help='classification method: one-vs-all OR one-vs-one')
    parser.add_argument("-i", "--info-prefix", required=True, type=str, action="store",
                        dest="info_prefix", help="informative prefix")
    args = parser.parse_args()

    extractor = None
    
    if args.method == 'one-vs-all':
        extractor = One_vs_All(args.info_prefix)
    else:
        extractor = One_vs_One(args.info_prefix)
    
    extractor.set_label_data(args.decision_values_file)
    extractor.populate_decision_values()
    extractor.roc_auc()
    