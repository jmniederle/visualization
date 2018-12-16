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

#np.seterr(divide='ignore', invalid='ignore')


array, df = read_data('profile_semantic_trafo_final.txt')
df1 = pd.DataFrame(array[1])
n_components = array.shape[1]
pca = PCA(n_components = n_components)
pca.fit(df1)
pca.components_.shape
components_df = pd.DataFrame(pca.components_)
components_df




#for i in pca.components_:
#    print(i.mean())
#
#X = array2[0]
#transformer = SparsePCA(n_components=array2.shape[1])
#transformer.fit(array2[0])
#X_transformed = transformer.transform(X)



