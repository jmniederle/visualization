<<<<<<< HEAD
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd
import storage_aggr as sa
import plotly.io as pio
import os
#import dash
#import dash_html_components as html
#import dash_core_components as dcc


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = sa.read_data('profile_semantic_trafo_final.txt')
dyn_graph_df = df.drop_duplicates(subset=['time', 'start', 'target'])[:2000]


lst =[]
for row in dyn_graph_df.iterrows():
    lst.append([row[1]['time'], row[1]['start'], (row[1]['time'] + 0.5), row[1]['target'], row[1]['logweight']])

dyn_graph_df =pd.DataFrame(lst)

traces = []
for row in dyn_graph_df.iterrows():
    traces.append(go.Scatter(
            x = [row[1][0], row[1][2]],
            y = [row[1][1], row[1][3]],
            mode= 'lines'))

fig = go.Figure(data=traces)
py.iplot(fig, filename='news-source')

if not os.path.exists('images'):
    os.mkdir('images')
pio.write_image(fig, 'images/fig1.png')

'''
app.layout = html.Div(dcc.Graph(id='dyn_graph',
                                figure={
                                        'data': [
                                                go.Scatter(
                                                    x = [rows[1][0], rows[1][2]],
                                                    y = [rows[1][1], rows[1][3]],
                                                    mode= 'lines'
                                                    ) for rows in dyn_graph_df.iterrows()
                                            ]
                                        }
    ))
=======
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

                    html.Div([html.H5('Select start node'),
                              dcc.Dropdown(id='dyn_start_node',
                                           options=[{'label': i, 'value': i} for i in data['start'].sort_values().unique()],
                                           value=data['start'].min())
                              ], className = 'six columns'),
                    
                    html.Div([html.H5('Select end start node'),
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
        for edge in range(df['cat_time'].describe()['freq']):
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
                    y_trace.append(None)
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
                                mode= 'lines'
                                ) for trace in lst2
                        ],
                    'layout':
                         go.Layout(
                                 title='Dynamic Graph Visualisation',
                                 showlegend = False)                                           
                    }
        return returnval
>>>>>>> d5115ac2f380a314a52da9049c688edfe25432d7


if __name__ == '__main__':
    app.run_server(debug=True)
<<<<<<< HEAD
'''
=======



#df['time'] = df['time'].astype('category')
#df['time'].describe()
>>>>>>> d5115ac2f380a314a52da9049c688edfe25432d7
