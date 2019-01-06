import storage_aggr as sa
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix

df = sa.read_data("profile_semantic_trafo_final.txt")

array = sa.aggregate(df)
zero_l = [0 for i in range(0, 983)]
A = np.vstack([array, zero_l])
A = np.vstack([A, zero_l])

matr = csr_matrix(A)



perm = reverse_cuthill_mckee(matr)
test = A[np.ix_(perm,perm)]
np.shape(test)
aggr_df = sa.array_to_df(test)

#arr_perm = A[perm, perm]
#np.shape(arr_perm)
#arr_perm


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        dcc.Graph(figure={
                'data':[
                    go.Scatter(
                        x = aggr_df['start'],
                        y = aggr_df['target'],
                        mode = 'markers',
                        marker = dict(
                                color = aggr_df['logweight'],
                                reversescale = True,
                                showscale=True))
                    ],
                'layout':
                    go.Layout(
                    title='Aggregated Adjacency Matrix Visualisation',
                    xaxis={
                            'title':'start',
                            'showgrid' : True,
                            'zeroline' : True,
                            'showline' : True,
                            'mirror' : 'ticks' 
                        },
                    yaxis={
                            'title':'target',
                            'showgrid':True,
                            'zeroline' : True,
                            'showline' : True
                        }
                    )
                            
                })
        ])
                    
                    
if __name__ == '__main__':
    app.run_server(debug=True)
