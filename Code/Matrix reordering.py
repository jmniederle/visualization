# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 11:59:43 2018

@author: 20175848
"""
import numpy as np
#from matplotlib.mlab import PCA
from storage_aggr import aggregate, read_data
import sklearn
import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import SparsePCA
import pandas as pd
from collections import Counter


#np.seterr(divide='ignore', invalid='ignore')
##############################################################################
#array, df = read_data('profile_semantic_trafo_final.txt')
#data = pd.DataFrame(aggregate(df, t_min = 64, t_max = 65, agg_type = "max"))
#data = data + 1
#data = np.log(data)
#transformer = SparsePCA(n_components = 1)
#transformed = transformer.fit_transform(data)
#df_components = pd.DataFrame(transformer.components_)
#df_components = abs(df_components)
#df_components = df_components.sort_values(by=0, ascending=False, axis=1)
#df_components.max().idxmax()
#
#data = aggregate(df, t_min = 64, t_max = 65, agg_type = "max")
#data = sorted(data, key=lambda x: x[df_components.max().idxmax()])
#data
def PCA_sort(filename):
    array, df = read_data(filename)
    data = pd.DataFrame(aggregate(df, t_min = 64, t_max = 65, agg_type = "max"))
    data = data + 1
    data = np.log(data)
    transformer = SparsePCA(n_components = 1)
    transformed = transformer.fit_transform(data)
    df_components = pd.DataFrame(transformer.components_)
    df_components = abs(df_components)
    df_components = df_components.sort_values(by=0, ascending=False, axis=1)
    df_components.max().idxmax()
    data = aggregate(df, t_min = 64, t_max = 65, agg_type = "max")
    data = sorted(data, key=lambda x: x[df_components.max().idxmax()])
    return(data)
print(PCA_sort('profile_semantic_trafo_final.txt'))
    
    
###############################################################################
#from sklearn.cluster import AgglomerativeClustering
#import matplotlib.pyplot as plt  
##%matplotlib inline
#data.head()
#cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')  
#cluster.fit_predict(df)
#plt.figure(figsize=(10, 7))  
#plt.scatter(df['start'], df['target'], c=cluster.labels_, cmap='rainbow')

###############################################################################
#array2 = array + 1

# Maakt een lijst met de hoogste PCA component voor elke timestamp
#component_list = []
#for i in array2:
#    df1 = pd.DataFrame(i)
#    #n_components = 'mle'
#    pca = PCA(n_components = 1)
#    pca.fit(df1)
#    pca.components_.shape
#    components_df = pd.DataFrame(pca.components_)
#    component_list.append(components_df.max().idxmax())

# Kijkt welke attribute het vaakst de hoogste CPA score heeft
# Hier moet dus op gesort worden
<<<<<<< HEAD
    
data = Counter(component_list)
print(data.most_common(1))

=======
#    
#data = Counter(component_list)
#data.most_common(1)
>>>>>>> aff0c43078e8f665b351f37a70902aa72e510df6


#for i in pca.components_:
#    print(i.mean())
#
#X = array2[0]
#transformer = SparsePCA(n_components=array2.shape[1])
#transformer.fit(array2[0])
#X_transformed = transformer.transform(X)



