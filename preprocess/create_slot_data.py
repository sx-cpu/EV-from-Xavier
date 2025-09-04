import pandas as pd
import os
from handles.data_hand import get_csv_data


import json
config = json.load(open('config.json'))

def get_data_time(data, datetime_col_name,suffix):
    
    df = pd.DataFrame()
    df['day'] = pd.to_datetime(data[datetime_col_name]).dt.day
    df['month'] = pd.to_datetime(data[datetime_col_name]).dt.month
    df['year'] = pd.to_datetime(data[datetime_col_name]).dt.year
    df['DOY'] = pd.to_datetime(data[datetime_col_name]).dt.strftime('%j')
    df['Weekday'] = pd.to_datetime(data[datetime_col_name]).dt.weekday
    df['time_slot'] = ( (pd.to_datetime(data[datetime_col_name]) - 
                         pd.to_datetime(data[datetime_col_name]).dt.floor('D')).dt.total_seconds()) / 3600
    df.columns = [suffix + col for col in df.columns]
    return df



def get_processed_data(raw_data):
    start = get_data_time(data=raw_data, datetime_col_name='Started', suffix='Start_')
    # end = get_data_time(data=raw_data, datetime_col_name='Ended', suffix='End_')

    # These are the energy requirment and departure times
    energy = raw_data['TotalEnergy']
    departure = raw_data['ConnectedTime']

    # Pole data
    pole = raw_data['ChargePoint']

    # Here we combine the data to form a processed dataframe
    p_data = pd.concat([start.reset_index(drop=True),
                        energy.reset_index(drop=True),
                        departure.reset_index(drop=True),
                        pole.reset_index(drop=True)], axis=1)
    return p_data

def get_slotted_array(data, slot_secs):
    # created slots are in form of ceilings.
    factor = slot_secs/3600
    # columns_to_divide = ['Start_time_slot', 'ChargeTime', 'ConnectedTime']
    data['Start_time_slot'] = ((data['Start_time'] // factor)+1).astype(int)
    data['Energy_required_slot'] = ((data['Energy_required'] // factor)+1).astype(int)
    data['Connected_time_slot'] = ((data['Connected_time'] // factor)+1).astype(int)
    return data


# ---------------------------------------------------------------------------------------------------- #
# The main function.
# this will pull the arguments, get the raw data, create a processed data and slotted data
# slots create are in the form of ceilings. i.e. for a 15 minute slots, 23 minutes is the 2nd slot.
def create_slot_data():
    raw_filename = config['transactions_filename']
    raw_filepath = os.path.join(os.getcwd(),config["dir_names"]["res_folder_name"])
    slot_minutes = config['slot_mins']
    save_location = os.path.join(os.getcwd(),config["dir_names"]["preprocess_folder_name"])
    save_file_name = "Slot_"+str(slot_minutes)+"_min_trans_data.csv"


    if os.path.exists(os.path.join(save_location,save_file_name)):
        if config['verbose'] > 1:
            print(' ------------------- Slotted data already present : Slots of ' + str(slot_minutes) +
                  ' minutes -------------------')
        return save_file_name,save_location
    
    else:

        # get raw data
        raw_data = get_csv_data(filename=raw_filename, filepath=raw_filepath)

        # process the raw data file
        processed_data = get_processed_data(raw_data=raw_data)
        processed_data.columns = ['Start_day', 'Start_month', 'Start_year', 'Start_DOY','Start_weekday', 'Start_time', 'Energy_required',
                                  'Connected_time', 'Charge_point']

        # create slotted data file from processed data file
        slotted_data = get_slotted_array(data=processed_data, slot_secs=slot_minutes * 60)

        # Cleaning the data.
        if config['data_collector'] == 'Y':
            processed_data = slotted_data[slotted_data.Energy_required != 0]
            processed_data['Departure_time'] = processed_data['Start_time'] + processed_data['Connected_time']
            processed_data = processed_data[processed_data.Departure_time <= processed_data.Start_time + 24]



