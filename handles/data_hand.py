import pandas as pd
import os

import json

config = json.load(open('config.json'))

def get_csv_data(filename, filepath):
    # This function returns the data. data format should be in csv
    # read the raw data and prepare print out the first five rows of the data

    raw_data = pd.read_csv(os.path.join(filepath, filename))
    if config['verbose'] > 2:
        print(" ------------------- File:",filename," -------------------")
        print(raw_data.head(1))
    return raw_data
        
