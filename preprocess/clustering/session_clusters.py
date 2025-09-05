import pandas as pd
from handles.data_hand import get_csv_data
import os

# load the config file
import json
config = json.load(open('config.json'))

# The main function
def session_clustering(slot_file_name, slot_file_path):

    Year = config['Year']
    slot_file_name = slot_file_name
    slot_file_path = slot_file_path
    save_name = "Final_session_clustered_" + str(Year) + "_trans_data.csv"
    save_location = os.path.join(os.getcwd(), config['dir_names']['preprocess_folder_name'], 'session_cluster')
    monthclust_file = 'Monthly_clustered_' + str(Year) + '_trans_data.csv'
    monthclust_filepath = os.path.join(os.getcwd(), config["dir_names"]["preprocess_folder_name"], 'session_cluster')
   

    # check if the final clustered file exists or not
    if os.path.exists(os.path.join(save_location, save_name)):
        if config['verbose'] > 1:
            print(' ------------------- Annual clusters exist ------------------------')
            print(" \t\t Final Clustered Data Saved as: ",
                  os.path.join(save_location, save_name))
            print(' \t\t Clusters Created for year :' + str(Year))
        return save_name, save_location

    else:

        # ------------------------------------------ Monthly Clusters --------------------------------------------------
        # Check if monthly clusters are created. If not, create them

        if os.path.exists(os.path.join(monthclust_filepath, monthclust_file)):
            if config['verbose'] > 1: print(' ------------------- Monthly Cluster File Exists --------------------')
        else:
            if config['verbose'] > 1: print(' ------------------- Creating Monthly Cluster File --------------------')
        
        from preprocess.clustering.monthly_cluster_data_points import main as monthly_ses_clust
        monthly_ses_clust(slot_file_name=slot_file_name,
                          slot_file_path=slot_file_path,
                          save_loc = monthclust_filepath,
                          save_name = monthclust_file)
        
        if config['verbose'] > 1: print(" Monthly clustered Data Saved as: ",
                                         os.path.join(monthclust_filepath, monthclust_file))
