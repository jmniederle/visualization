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


array, df = read_data('profile_semantic_trafo_final.txt')
array2 = array + 1

# Maakt een lijst met de hoogste PCA component voor elke timestamp
component_list = []
for i in array2:
    df1 = pd.DataFrame(i)
    #n_components = 'mle'
    pca = PCA(n_components = 1)
    pca.fit(df1)
    pca.components_.shape
    components_df = pd.DataFrame(pca.components_)
    component_list.append(components_df.max().idxmax())

# Kijkt welke attribute het vaakst de hoogste CPA score heeft
# Hier moet dus op gesort worden
    
data = Counter(component_list)
print(data.most_common(1))



#for i in pca.components_:
#    print(i.mean())
#
#X = array2[0]
#transformer = SparsePCA(n_components=array2.shape[1])
#transformer.fit(array2[0])
#X_transformed = transformer.transform(X)



