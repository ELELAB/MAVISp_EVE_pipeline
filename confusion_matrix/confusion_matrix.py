import os
import yaml
import argparse
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt


#Open yaml file
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

#Processing of the EVE and Mavisp files
def read_files(eve_path,mavisp_path):
    eve_df= pd.read_csv(eve_path).loc[:,'EVE_classes_25_pct_retained_ASM']
    mavisp_df=pd.read_csv(mavisp_path).loc[:,'EVE_classes_25_pct_retained']
    final_df = pd.concat([eve_df, mavisp_df],axis=1).dropna()
    return final_df

#Calculation of the confusion matrix
def confusion_matrix_calculation(comparison_df):
    actual=comparison_df['EVE_classes_25_pct_retained_ASM'].to_numpy()
    predicted=comparison_df['EVE_classes_25_pct_retained'].to_numpy()
    c_matrix = confusion_matrix(actual, predicted)
 
    return c_matrix

def scores(con_matrix):
    #Extract values from the confusion matrix
    c00, c01, c02, c10, c11, c12, c20, c21, c22=np.ravel(con_matrix)
    
    #Precision of each class
    pathogenic_precision=c00/(c00+c01+c02)
    begign_precision=c10/(c10+c11+c12)
    uncertain_precision=c20/(c20+c21+c22)
    
    overall_precision = (pathogenic_precision + begign_precision + uncertain_precision) / 3
    
    #Recall of each class
    pathogenic_recall=c00/(c00+c10+c20)
    begign_recall=c11/(c11+c01+c21)
    uncertain_recall=c22/(c22+c12+c02)
    
    #F1 scores for each class
    pathogenic_f1_score=(2*pathogenic_precision*pathogenic_recall)/(pathogenic_precision+pathogenic_recall)
    begign_f1_score=(2*begign_precision*begign_recall)/(begign_precision+begign_recall)
    uncertain_f1_score=(2*uncertain_precision*uncertain_recall)/(uncertain_precision+uncertain_recall)
    
    overall_f1_score = (pathogenic_f1_score + begign_f1_score + uncertain_f1_score) / 3
    
    #Accuracy of each class
    pathogenic_accuracy=c00/(c01+c02)
    begign_accuracy=c11/(c10+c12)
    uncertain_accuracy=c22/(c20+c21)
    
    overall_accuracy = (c00+c11+c22) / (c00+ c01+c02+c10+c11+c12+c20+c21+c22)
    
    scores={
        "Precision":[pathogenic_precision,begign_precision,uncertain_precision],
        "Accuracy": [pathogenic_accuracy,begign_accuracy,uncertain_accuracy],
        "F1 score": [pathogenic_f1_score,begign_f1_score,uncertain_f1_score],
        "Overall scores": [overall_precision,overall_accuracy,overall_f1_score]
        }
    
    return scores
    

def create_resuts_table(scores_function,con_matrix):
    data = scores(con_matrix)
    column_data = [[data[key][i] for key in data] for i in range(3)]
    
    fig, ax = plt.subplots()

    # Create the table
    table_data = []
    
    # Add column names
    column_names = ['','Pathogenic', 'Begign', 'Uncertain']
    table_data.append(column_names)
    row_names = ['Precision', 'Accuracy', 'F1 score',"Overall score"]
    
    for i in range(4):
        row_data = [row_names[i]] + [f'{lst[i]:.3f}' for lst in column_data]
        table_data.append(row_data)
    
    # Create the table
    table = ax.table(cellText=table_data, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    table.get_celld()[(4,0)].set_facecolor("#56b5fd")
    
    ax.axis('off')
    
    plt.show()
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()

#Load configurations
    config = load_config(args.config)
    
#Path to the comparisons file  
    parent_directory=config['file_path']
        
        
    con_matrix=0
        
    subdirectories_paths = [os.path.join(parent_directory,subdir) for subdir in os.listdir(parent_directory) 
                    if os.path.isdir(os.path.join(parent_directory, subdir))]
    eve_files = [file for file in os.listdir(subdirectories_paths[0]) 
                if os.path.isfile(os.path.join(subdirectories_paths[0], file))]

    for file in eve_files:
        
        if os.path.exists(subdirectories_paths[1]):
            correspoding_file= os.path.join(subdirectories_paths[1], file)
            comparison_df=read_files(os.path.join(subdirectories_paths[0], file),correspoding_file)
            con_matrix+=confusion_matrix_calculation(comparison_df)
               
    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = con_matrix, 
                                                display_labels = ["Pathogenic","Benign","Uncertain"])

    cm_display.plot()
    plt.show()
    
    create_resuts_table(scores,con_matrix)

if __name__ == "__main__":
    main()