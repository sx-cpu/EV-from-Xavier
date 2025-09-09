# libraries

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from functools import reduce
from preprocess.clustering.pole_class import pole
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
        pole_class = pole(Clustered_filename=finalclust_file, Clustered_filepath=file_path)
        pv = pole_class.pivot_poles(col='Day_type')
        pv1 = pole_class.pivot_poles(col='Start_time_slot')
        pv2 = pole_class.pivot_poles(col='Final_clusters')
        pv2.columns = ['Charge_point','C0','C1','C2']
        pole_properties = reduce(lambda x, y: pd.merge(x, y, on='Charge_point', how='outer'), [pv, pv1, pv2])
        


        
