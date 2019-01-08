import pandas as pd
import numpy as np
import os

os.chdir('C:/Users/20175848/Dropbox/Data Science Y2/Q2/Visualization/visualization/Code')
data = pd.read_table('dataset_joshua.txt')
data['Weight'] = 1
data['time'] = 1
data.columns = ['start', 'target', 'weight', 'time']

for i in range(len(data)):
    data['time'][i] = i//1000
    print(data['time'][i])
    
data.tail()

data.to_csv('C:/Users/20175848/Dropbox/Data Science Y2/Q2/Visualization/Assignment 6/data_3.txt', sep='\t', encoding='utf-8')
