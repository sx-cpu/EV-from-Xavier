# Import required libraries
from sklearn.cluster import DBSCAN
import pandas as pd 
import numpy as np
import os
from handles.data_hand import get_csv_data



# load the config file
import json
config = json.load(open('config.json'))

class pole:
    def __init__(self, Clustered_filename, Clustered_filepath, pole_col_name = 'Charge_point'):
        # We will get the data and do some preprocessing. Here we will also add 2 extra columns.
        # 1) as a weekend/weekday indicator
        # 2) as a indicator of session
        self._data = get_csv_data(filename=Clustered_filename, filepath=Clustered_filepath)
        self._pole_col_name = pole_col_name
        # 2 extra columns
        self.weekdays_divide()
        self._data['Indicator'] = 1
        self._each_pole_data = self.split_data()


    def weekdays_divide(self):
        # This function will divide the weekends and weekdays into 0 and 1
        # df = pd.DataFrame()
        # df['Day_type'] = self._data['Start_weekday']
        # df.loc[self._data['Start_weekday'] < 5, 'Day_type'] = 'Weekday'
        # df.loc[self._data['Start_weekday'] > 4, 'Day_type'] = 'Weekend'
        # self._data['Day_type'] = df['Day_type']
        self._data['Day_type'] = np.where(self._data['Start_weekday'] < 5, 'weekday', 'Weekend')

    def split_data(self):
        # This splits the dataframe into various dataframes based on which pole the charging takes place in
        dfs = [rows for _, rows in self._data.groupby(self._pole_col_name)]
        return dfs

    def pivot_poles(self, col):
        # this will pivot the cols into rows. we can use the indicator variable to keep track of the total sessions

        # this is the group by 4 coulmuns and sum all the other columns
        df = self._data.groupby([col, 'Charge_point'], as_index=False).sum()
        df1 = df.pivot_table(columns=[col], index='Charge_point', values='Indicator',fill_value=0).reset_index()
        self._current_df = df1
        return df1
    
    