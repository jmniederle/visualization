# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


from storage_aggr import read_data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = read_data('profile_semantic_trafo_final.txt')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='time-slider',
                options=[{'label': i, 'value': i} for i in df['time'].unique()],
                value=1),
                
            dcc.Graph(
                id='dynamic-graph' 
                ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='time-slider2',
                options=[{'label': i, 'value': i} for i in df['time'].unique()],
                value=1),
                
            dcc.Graph(
                id='dynamic-graph2' 
                ),
        ],
        style={'width': '48%', 'float' : 'right', 'display': 'inline-block', 'vertical-align': 'top'})
    ])

])


@app.callback(
    dash.dependencies.Output('dynamic-graph', 'figure'),
    [dash.dependencies.Input('time-slider', 'value')])
def update_dy(timestamp): # inp_df toevoegen
    df = read_data('profile_semantic_trafo_final.txt')
    inp_df = df
    x_r, y_r = (inp_df['start'].max(), inp_df['target'].max())
    df = inp_df[inp_df['time']==timestamp]
    returnval = {
            'data':[
                go.Scatter(
                    x = df['start'],
                    y = df['target'],
                    mode = 'markers',
                    marker = dict(
                            color = df['logweight'],
                            colorscale='Viridis',
                            showscale=True))
                ],
            'layout':
                go.Layout(
                title='Adjacency Matrix Visualisation',
                xaxis={
                        'title':'start',
                        'showgrid' : True,
                        'zeroline' : True,
                        'showline' : True,
                        'range' : [0,x_r],
                        'mirror' : 'ticks' 
                    },
                yaxis={
                        'title':'target',
                        'showgrid':True,
                        'zeroline' : True,
                        'showline' : True,
                        'range':[y_r,0]
                    }
                )
                        
            }
    
    return returnval

@app.callback(
    dash.dependencies.Output('dynamic-graph2', 'figure'),
    [dash.dependencies.Input('time-slider2', 'value')])
def update_dy2(timestamp): # inp_df toevoegen
    df = read_data('profile_semantic_trafo_final.txt')
    inp_df = df
    x_r, y_r = (inp_df['start'].max(), inp_df['target'].max())
    df = inp_df[inp_df['time']==timestamp]
    returnval = {
            'data':[
                go.Scatter(
                    x = df['start'],
                    y = df['target'],
                    mode = 'markers',
                    marker = dict(
                            color = df['logweight'],
                            colorscale='Viridis',
                            showscale=True))
                ],
            'layout':
                go.Layout(
                title='Adjacency Matrix Visualisation',
                xaxis={
                        'title':'start',
                        'showgrid' : True,
                        'zeroline' : True,
                        'showline' : True,
                        'range' : [0,x_r],
                        'mirror' : 'ticks' 
                    },
                yaxis={
                        'title':'target',
                        'showgrid':True,
                        'zeroline' : True,
                        'showline' : True,
                        'range':[y_r,0]
                    }
                )
                        
            }
    
    return returnval


if __name__ == '__main__':
    app.run_server(debug=True)
