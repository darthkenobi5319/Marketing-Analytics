#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:30:47 2020

@author: xuzhixing
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#create dataframe with each order as a row
data = pd.read_csv('transactions_n100000.csv')
dataset = pd.pivot_table(data, index= 'ticket_id', columns ='item_name', values='item_count', aggfunc = np.sum)
data.drop_duplicates(subset=['ticket_id', 'order_timestamp', 'location', 'lat', 'long'], inplace=True)
dataset = pd.merge(dataset, data[['ticket_id', 'order_timestamp', 'location', 'lat', 'long']], on='ticket_id', how='left')
dataset.fillna(0, inplace=True)

#transfer order_timestamp into datetime
dataset['order_timestamp'] = pd.to_datetime(dataset['order_timestamp'])
dataset['dow'] = [i.weekday() for i in dataset['order_timestamp']]
dataset['year'] = [i.year for i in dataset['order_timestamp']]
dataset['month'] = [i.month for i in dataset['order_timestamp']]
dataset['day'] = [i.day for i in dataset['order_timestamp']]
dataset['hour'] = [i.hour for i in dataset['order_timestamp']]

#add dummy variables for hourly
dataset['11-13'] = 0
dataset['14-16'] = 0
dataset['17-19'] = 0
dataset['20-22'] = 0
dataset['23-1'] = 0

for index,row in dataset.iterrows():
    if row['hour'] in [11,12,13]:
        dataset.at[index, '11-13'] = 1
    elif row['hour'] in [14,15,16]:
        dataset.at[index, '14-16'] = 1
    elif row['hour'] in [17,18,19]:
        dataset.at[index, '17-19'] = 1
    elif row['hour'] in [20,21,22]:
        dataset.at[index, '20-22'] = 1
    elif row['hour'] in [23,0,1]:
        dataset.at[index, '23-1'] = 1

#add dummy variables for location
dataset['central'] = 0
dataset['station&parking'] = 0
dataset['sub'] = 0
dataset['university'] = 0

for index,row in dataset.iterrows():
    if row['location'] in [1,3,7]:
        dataset.at[index, 'central'] = 1
    elif row['location'] in [5,6]:
        dataset.at[index, 'station&parking'] = 1
    elif row['location'] in [4,9]:
        dataset.at[index, 'sub'] = 1
    elif row['location'] in [2,8]:
        dataset.at[index, 'university'] = 1

#define function to find the best k number        
def fitting(df):
    Sum_of_squared_distances = []
    K = range(1,15)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(df)
        Sum_of_squared_distances.append(km.inertia_)
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()
    return 

df_3 = dataset[['burger','fries','salad','shake', '11-13','14-16', '17-19', '20-22', '23-1', 'central', 'station&parking',
               'sub', 'university']]

fitting(df_3)

#using KMeans Clustering with n_clusters = 3
kmeans = KMeans(n_clusters = 3, random_state=0).fit(df_3)

result = pd.DataFrame(kmeans.cluster_centers_, columns = ['burger','fries','salad','shake', '11-14','14-17', 
                                                     '17-20', '20-23', '23-2', 'cbd', 'station&parking',
               'suburban-center', 'university_area'])

print(result)

