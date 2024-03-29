import pandas as pd
import numpy as np

def read_data(filename):

    df = pd.read_csv(filename, sep = ' ', index_col = False)

    data = np.zeros((1232, 981, 983), np.float64)

    for row in df.iterrows():
        time = row[1][0]
        start = row[1][1]
        target = row[1][2]
        weight = row[1][3]
        
        data[time][start][target] += weight

    return (data, df)


def aggregate(pd_df, t_min = 0, t_max = None, agg_type = "sum"):
    #pd_df.sort_values(by="time", inplace=True)
    
    assert(agg_type in ["sum", "mean", "min", "max"]), "agg_type can be either: sum, mean, min, max"
    assert(type(t_min) == int), "t_min has to be an integer"
    if t_max != None:
        assert(type(t_max) == int), "t_max has to be an integer"
    
    
    if t_max == None:
        t_max = max(pd_df['time']) + 1
    
    s_l, t_l = (max(pd_df['start']) + 1, max(pd_df['target']) + 1)
    
    pd_df = pd_df[(pd_df['time'] >= t_min) & (pd_df['time'] <= t_max)]
    
    w_matr = np.zeros((s_l, t_l))
    
    
    if (agg_type == "sum" or agg_type == "mean"):
        c_matr = np.zeros((s_l, t_l))
        
        for row in pd_df.iterrows():
            w_matr[row[1]['start']][row[1]['target']] += row[1]['weight']
            c_matr[row[1]['start']][row[1]['target']] += 1
        
        if agg_type == "sum":
            return w_matr 
        
        return np.divide(w_matr, c_matr, where = (c_matr != 0))
    
    
    elif (agg_type == "min"):
        for row in pd_df.iterrows():
            cur_w = w_matr[row[1]['start']][row[1]['target']] 
            row_w = row[1]['weight']
            
            if (row_w < cur_w) or (cur_w == 0):
                w_matr[row[1]['start']][row[1]['target']] = row[1]['weight']
            
        return w_matr
    
    
    elif (agg_type == "max"):
        for row in pd_df.iterrows():
            cur_w = w_matr[row[1]['start']][row[1]['target']] 
            row_w = row[1]['weight']
            
            if row_w > cur_w:
                w_matr[row[1]['start']][row[1]['target']] = row[1]['weight']
            
        return w_matr
    
    raise Exception("No if statement was executed.")
    


if __name__ == "__main__":
    array, df = read_data('profile_semantic_trafo_final.txt')
    
    a = aggregate(df, t_min = 64, t_max = 65, agg_type = "min")#[76][89]   
    a.shape
       
