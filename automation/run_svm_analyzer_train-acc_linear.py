'''
Created on Jan 19, 2013

@author: mandar
'''
import stdout_data_extractor as StdoutParser

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='SVM analyzer with train-acc-linear method')
    parser.add_argument("-sf", "--stdout-file", required=True, type=str, action="store",
                        dest='stdout_file', help='stdout.txt file path')
    parser.add_argument("-df", "--decision-values-file", required=True, type=str, action="store",
                        dest="decision_values_file", help="decision_values.csv file path")
    args = parser.parse_args()
    
    