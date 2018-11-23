import pandas as pd
import numpy as np

def read_data(filename):
    
    df = pd.read_csv(filename, sep = ' ', index_col = False)
    
    data = np.zeros((1232, 981, 983), np.int32)  
    
    for row in df.iterrows():
        time = row[1][0]
        start = row[1][1]
        target = row[1][2]
        weight = row[1][3]
        
        data[time][start][target] = weight
    
    return data

data = read_data('./profile_semantic_trafo_final.txt')

