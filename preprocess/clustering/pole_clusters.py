# libraries

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# load the config flie
import json
config = json.load(open('config.json'))

# The main function
def pole_clustering(ses_clust_file_path, ses_clust_file_name):
    Year = config['Year']
    annual_sessions_cutoff = 0
    Combine_start_slots = 4
    Clustering_on = 'Percentage'                                # what to cluster with
    Cluster_by = 'Session_clusters'                             # 'Which parameters to cluster the data by:


    finalclust_file = ses_clust_file_name
    file_path = ses_clust_file_path
    save_location = os.path.join(os.getcwd(), config["dir_names"]["preprocess_folder_name"], 'pole_cluster')
    save_name = "Poles_clustered_" + str(Year) + "_by" + Cluster_by + "_cutoff " + str(
        annual_sessions_cutoff) + ".csv"

    if os.path.exists(os.path.join(save_location,save_name)):
        if config['verbose'] > 1: print(' ------------------- Pole Cluster File Exists --------------------')
        return save_name,save_location
    else:
        # CREATING POLES CLUSTERS ---------------------------------------------------------------------------------
        if config['verbose'] > 1: print(' ------------------- Creating Pole Cluster File --------------------')
        
