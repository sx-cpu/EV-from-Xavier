# Import required libraries
import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import preprocess.clustering.my_dbscan as my_dbscan
from handles.data_hand import get_csv_data

# load the config file
import json
config = json.load(open('config.json'))

def main(slot_file_name, slot_file_path, save_loc, save_name):

    slot_filename = slot_file_name
    slot_filepath = slot_file_path
    Year = config['Year']
    save_location = save_loc
    save_name = save_name
  
    # These are the parameters for dbscan. Use them carefully
    ep = 5
    alpha = 0.005
    minpoints = 45

    #1 0.05 440
    #8 0.51 30

    if os.path.exists(os.path.join(save_location,save_name)):
        if config['verbose'] > 2:
            print(' ------------------- Monthly clusters exist ------------------------')
        return
    else:

        # ------------------------------------------Preprocess data for dbscan ----------------------------------------
        # Create data properly. We take data from jan to dec.
        # However, in the 'Y' dataset, we only have data from 2021/9 to 2022/9
        # This data is cleaned such that charging timees are realistic and less than 24 hours. We also make sure that
        # no car stays more than 24 hours. Year is the only parameter defined as input, all other parameters
        # should be changed from inside the code

        X = get_csv_data(filename=slot_filename, filepath=slot_filepath)
        temp = X[X.Start_year == Year]
        temp = temp[temp.Start_month < 13]
        processed_data = temp.reset_index()

        temp2 = processed_data[['Start_time', 'Departure_time', 'Start_month', 'index']]
        Data_for_dbscan = temp2
        if config['verbose'] > 2:
            print(' ------------------- Total number of sessions for clustring: ', len(Data_for_dbscan))
            print(' ------------------- Session clustring for year: '+str(Year))

        # --------------------------------Create a dbscanner and cluster data------------------------------------------
        # dbscanner from class created in my_dbscan. We will not normalize the data and take ep = 8 and min points =
        # 30 in each cluster.

        db_temp = my_dbscan.mydbscan(epsilon=ep, min_points=minpoints, alpha=alpha)
        db_temp.data(data=Data_for_dbscan,norm=False)
        db_temp.create_clusters()

        # Save Clusters
        processed_data = processed_data.join(pd.concat(db_temp._monthly_clusters).set_index('index'), on='index')
        processed_data.to_csv(os.path.join(save_location, save_name), index=False)

        # Plot and save the plot for future references
        if config['create_plots']:
            colors = np.array(processed_data[['Clusters']])
            plt.scatter(processed_data[['Start_time']], processed_data[['Departure_time']],
                                     c= colors, cmap='Paired',s=0.2)
            plt.savefig(os.path.join(save_location, 'Monthly_clust_' + str(Year) + '_plot.png'))
                        









