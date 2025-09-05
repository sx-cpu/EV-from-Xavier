# We create monthly clusters for sessions using this mydbscan file

# libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

# load the config file
import json
config = json.load(open('config.json'))


class mydbscan:
    # This class is used to implement dbscan for us

    def __init__(self, epsilon, min_points, alpha):
        self._ep = epsilon
        self._minpts = min_points
        self._dbscan = []
        self._monthly_clusters = []
        self._alpha = alpha
        self._monthly_eps = []


    
    def data(self, data, norm=True):
        # Input data should be just columns of the points that need to be clustered. nothing else.

        if norm:
            # Scaling the data to bring all the attributes to a comparable level. Converting the numpy array into a
            # pandas DataFrame
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform()
            norm_data = normalize(scaled_data)
            self._data = pd.DataFrame(norm_data)
        else:
            self._data = pd.DataFrame(data)          
        
    
    def create_clusters(self, how_many = 4):
        # This function creates the DB scan of the points. We force each month to have a given
        # number of clusters, i.e. how_many clusters. also, after the clustring is over, we alsorecord the epsilon
        # value for that month to create that many clusters.   
        # Create a monthly data, generate its clusters and add them to the monthly clusters file

        months = sorted(self._data['Start_month'].unique())
        for i in months:
            month_data = self._data[self._data.Start_month == i].copy()
            month_data1 = month_data[['Start_time', 'Departure_time']]

            if month_data1.empty:
                if config['verbose'] > 0:
                    print(f'month {i} has no data')
                continue

            if config['verbose'] > 2:
                print(" \t\t Clustering for month:", i)

            epsilon = self._ep

            # Here we force all months to have the same number of clusters
            while True:
                db_created = DBSCAN(eps=epsilon, min_samples=self._minpts).fit(month_data1)
                epsilon = epsilon-self._alpha
                if config['verbose'] > 2: print(" \t\t Clusteres Created :",np.unique(db_created.labels_))
                if len(np.unique(db_created.labels_)) == how_many or epsilon < 0:
                    if epsilon < 0:
                        if config['verbose'] > 2: print(" \t\t ","Specified number of clusters not found -- ")
                    if len(np.unique(db_created.labels_)) == how_many:
                        if config['verbose'] > 2: print(" \t\t ","3 clusters found -- ")
                    self._monthly_eps.append([i,epsilon])
                    break

            self._dbscan.append(db_created)
            month_data['Clusters'] = db_created.labels_
            self._monthly_clusters.append(month_data[['index', 'Clusters']])



            





