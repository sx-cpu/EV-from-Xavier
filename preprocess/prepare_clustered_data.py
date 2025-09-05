import os
from handles.data_hand import get_csv_data
from preprocess.clustering.session_clusters import session_clustering
from preprocess.create_slot_data import create_slot_data



import json
config = json.load(open('config.json'))

def create_processed_data():

    # Name and location of the final saved file
    save_name = 'Processed_' + str(config['slot_mins']) + '_min_' + str(config['Year']) + '_year_trans_data.csv'
    save_loc = os.path.join(os.getcwd(), config["dir_names"]["preprocess_folder_name"])

    if os.path.exists(os.path.join(save_loc, save_name)):
        # if the data is already generated, then we dont need to worry
        if config['verbose']>0: print(' ------------------- Processed Data File Exists -------------------')

    else:
        if config['verbose'] > 0: print(' ------------------- Creating Processed Data File -------------------')
        
        # call slotting script. this will create the slotted data that we need from transactions
        slot_file_name, slot_file_loc = create_slot_data()

        # call session clustering script. This will generate the session clusters
        ses_clust_file_name, ses_clust_file_path = session_clustering(slot_file_path=slot_file_loc,
                                                                       slot_file_name=slot_file_name)

   