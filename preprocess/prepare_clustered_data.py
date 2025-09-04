import os



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
        
