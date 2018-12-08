# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.io as pio
import os

from storage_aggr import aggregate, read_data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

array, df = read_data('profile_semantic_trafo_final.txt')


a = aggregate(df, t_min = 0, t_max = 100, agg_type = "max")
a += 1
a = np.log(a)

plotdata = [go.Heatmap(z=a, colorscale='Viridis')]#.tolist())]

fig = go.Figure(data=plotdata)
#py.iplot(fig, filename='testheatmap')
if not os.path.exists('images'):
    os.mkdir('images')
pio.write_image(fig, 'images/fig1.png')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    dcc.Graph(
        id='density_aggr', 
        figure={
            'data': [
                go.Scatter(
                    x=df['start'],
                    y=df['target']
                    )
                ]
            }
        )
    
])


'''
plotdata = pd.DataFrame(a)
plotdata = plotdata + 1
plotdata = plotdata.applymap(np.log)  
plotdata = [go.Heatmap( z=plotdata.values.tolist(), colorscale='Viridis')]

py.iplot(plotdata, filename='pandas-heatmap')'''


if __name__ == '__main__':
    app.run_server(debug=True)
