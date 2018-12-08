#import pandas as pd
import storage_aggr as sa

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
                        html.Div(children = [html.H4('Starting time'),
                                 dcc.Dropdown(
                                    id='dyn-dropdown',
                                    options= [{'label': i, 'value': i} for i in data['time'].unique()],
                                    value=1)],
                        style={'width': '30%', 'display': 'inline-block'}),
                        
                        html.Div(children = [html.H4('Ending time'),
                                 dcc.Dropdown(
                                    id='dyn-dropdown-2', 
                                    options= [{'label': i, 'value': i} for i in data['time'].unique()],
                                    value=1231)],
                                style={'width': '30%', 'float' : 'right', 'display': 'inline-block', 'vertical-align': 'top'}),
                        
                        html.Div(children= [html.H4('Select Log-weight'),
                                  dcc.Input(id='dyn_edge', value=data['logweight'].min(), type='number')],
                                style={'width': '30%', 'float' : 'right', 'display': 'inline-block'})
                        
                    ]),
                    html.Button('Plot', id='dyn_Button', n_clicks=0),
                    dcc.Graph(id='dyn_graph')
                    
                    #dcc.Slider(id='dyn_slider',
                               #min=data['logweight'].min(),
                               #max=data['logweight'].max(),
                               #value= data['logweight'].min())
                ])
        ])


@app.callback(Output('dyn_graph', 'figure'),
              [Input('dyn_Button', 'n_clicks'), Input('dyn-dropdown', 'value'),
               Input('dyn-dropdown-2', 'value'), Input('dyn_edge', 'value')])
def update_dyn(n_clicks, t_min, t_max, weight):
    if n_clicks > 0:
        df = sa.read_data('profile_semantic_trafo_final.txt')
        df = df.drop_duplicates(subset=['time', 'start', 'target'])
        df = df[(df['time'] >= t_min) & (df['time'] <= t_max) & (df['logweight'] >= weight)]
        
        start = time.time()
        lst2 = []
        for edge in range(5): # highest count of edges for time(639)
            print(edge)
            trace_dict = {}
            x_trace = []
            y_trace = []
            for timestamp in df['time'].unique():
                df1 = df[df['time'] == timestamp]
                try:
                    row = df1.iloc[edge]
                    x_trace.append(row['time'])
                    x_trace.append(row['time'] + 0.5)
                    y_trace.append(row['start'])
                    y_trace.append(row['target'])
                    #y_trace.append(None)
                except:
                    y_trace.append(None)
                    pass
            trace_dict['x'] = x_trace
            trace_dict['y'] = y_trace
            lst2.append(trace_dict)
        print(start - time.time())
        returnval = {
                    'data': [
                            go.Scatter(
                                x = trace['x'],
                                y = trace['y'],
                                connectgaps = False,
                                opacity= 0.7,
                                mode= 'lines',
                                ) for trace in lst2
                        ],
                    'layout':
                         go.Layout(
                                 title='Dynamic Graph Visualisation',
                                 showlegend = False)                                           
                    }
        return returnval


if __name__ == '__main__':
    app.run_server(debug=True)



#df['time'] = df['time'].astype('category')
#df['time'].describe()