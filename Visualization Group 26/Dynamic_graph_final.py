#import pandas as pd
import storage_aggr as sa
import numpy as np
import time
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

data = sa.read_data('profile_semantic_trafo_final.txt')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
            html.Div([
                html.Div([
                        html.Div(children = [html.H5('Starting time'),
                                 dcc.Dropdown(
                                    id='dyn-dropdown',
                                    options= [{'label': i, 'value': i} for i in data['time'].unique()],
                                    value=1)], className = 'six columns'),
                        
                         html.Div([html.H5('Ending time'),
                             dcc.Dropdown(
                                id='dyn-dropdown-2', 
                                options= [{'label': i, 'value': i} for i in data['time'].unique()],
                                value=1231)], className = 'six columns'
                            )
                 
                        
                    ], className = 'row'),
                             
                html.Div([
                    
                html.Div([html.H5('Select starting Log-weight'),
                        dcc.Input(id='dyn_edge_start', value=data['logweight'].min(), type='number',
                            #style={'width': '40%','float':'right', 'display': 'inline-block'}
                            )
                        ], className = 'six columns'),
                       

                    html.Div([html.H5('Select ending Log-weight'),
                                dcc.Input(id='dyn_edge_end', value=data['logweight'].max(), type='number',
                                    #style={'width': '40%', 'float' : 'right', 'display': 'inline-block'}
                                    )], className = 'six columns')
                            ], className = 'row'),

                html.Div([

                    html.Div([html.H5('Select first start node'),
                              dcc.Dropdown(id='dyn_start_node',
                                           options=[{'label': i, 'value': i} for i in data['start'].sort_values().unique()],
                                           value=data['start'].min())
                              ], className = 'six columns'),
                    
                    html.Div([html.H5('Select last start node'),
                              dcc.Dropdown(id='dyn_start_end_node',
                                           options=[{'label': i, 'value': i} for i in data['target'].sort_values().unique()],
                                           value=data['start'].max())
                              ], className = 'six columns')
                ], className= 'row'),

                html.Div([
                    html.Button('Plot', id='dyn_Button', n_clicks=0),
                    dcc.Graph(id='dyn_graph')])
                ])
        ])



@app.callback(Output('dyn_graph', 'figure'),
              [Input('dyn_Button', 'n_clicks'), Input('dyn-dropdown', 'value'),
               Input('dyn-dropdown-2', 'value'), Input('dyn_edge_start', 'value'),
               Input('dyn_edge_end', 'value'), Input('dyn_start_node', 'value'),
               Input('dyn_start_end_node', 'value')])
def update_dyn(n_clicks, t_min, t_max, weight_start, weight_end, start_node, end_node):
    if n_clicks > 0:
        print(n_clicks)
        df = sa.read_data('profile_semantic_trafo_final.txt')
        df = df.drop_duplicates(subset=['time', 'start', 'target'])
        df = df[(df['time'] >= t_min) & (df['time'] <= t_max) & (df['logweight'] >= weight_start) &
                (df['logweight'] <= weight_end) & (df['start'] >= start_node) & (df['start'] <= end_node)]
        df['cat_time'] = df['time'].astype('category')

        start = time.time()
        lst2 = []
        weightlst = []
        for timestamp in df['time'].unique():
            print(timestamp)
            df1 = df[df['time'] == timestamp]
            trace_dict = {}
            x_trace = []
            y_trace = []
            for edge in range(len(df1)):              
                row = df1.iloc[edge]
                x_trace.append(row['time'])
                x_trace.append(row['time'] + 5)
                y_trace.append(row['start'])
                y_trace.append(row['target'])
                y_trace.append(None)

            trace_dict['x'] = x_trace
            trace_dict['y'] = y_trace
            lst2.append(trace_dict)
            weightlst.append(np.mean(df1['logweight']))
        print(start - time.time())
        weights = np.array(weightlst)
        weights = list((weights/(weights.max()))*5)
        lst2 = zip(lst2, weights)
        
        returnval = {
                    'data': [
                            go.Scatter(
                                x = trace['x'],
                                y = trace['y'],
                                connectgaps = False,
                                opacity= 0.5,
                                mode= 'lines',
                                line = {'width': weight}
                                ) for trace, weight in lst2
                        ],
                    'layout':
                         go.Layout(
                                 title='Dynamic Graph Visualisation',
                                 showlegend = False,
                                 xaxis = {'type': 'category', 'tickangle': 45,
                                          'rangeslider': {'visible': True}}})                                           
                    }
        return returnval


if __name__ == '__main__':
    app.run_server(debug=True)