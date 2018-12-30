# -*- coding: utf-8 -*-
from sklearn.decomposition import TruncatedSVD
#from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix
from storage_aggr import aggregate, array_to_df


def matr_re(df, n_comp, time0, time1):
    dat = aggregate(df, time0, time1)
    #X = StandardScaler().fit_transform(dat)
    # Make sparse matrix
    X_sparse = csr_matrix(dat)
    
    # Create a TSVD
    tsvd = TruncatedSVD(n_components=n_comp)
    
    # Conduct TSVD on sparse matrix
    X_sparse_tsvd = tsvd.fit(X_sparse).transform(X_sparse)
    

    
    return array_to_df(X_sparse_tsvd)
