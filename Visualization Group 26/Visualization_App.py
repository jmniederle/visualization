# -*- coding: utf-8 -*-
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import pandas as pd
import base64
import io
import storage_aggr as sa
import dijkstra
import node_link_fnc as nl
import dim_red as dr

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

tab_1_layout = html.Div([
            html.H1('Data selecting and preprocessing'),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
            # Allow multiple files to be uploaded
            multiple=False
            ),
            # Hidden division
            html.Div(id='table')
        ])

tab_2_layout = html.Div([
            html.Div([
                html.Div([
                        html.Div(children = [html.H4('Starting time'),
                                 dcc.Dropdown(
                                    id='aggr-slider-dropdown', value=1)],
                        style={'width': '48%', 'display': 'inline-block'}),
                        
                        html.Div(children = [html.H4('Ending time'),
                                 dcc.Dropdown(
                                    id='aggr-slider-dropdown-2', value=1)],
                        style={'width': '48%', 'float' : 'right', 'display': 'inline-block', 'vertical-align': 'top'}),
                        
                    ]),
                html.Div([html.H5('Color Scale'),
                         dcc.RadioItems(id='aggr_scale',
                        options=[
                            {'label': 'Jet', 'value': 'Jet'},
                            {'label': 'Viridis', 'value': 'Viridis'},
                            {'label': 'YlOrRd', 'value':'YlOrRd'}
                        ],
                        value='YlOrRd')
                    ]),
                    html.Button('Plot', id='aggr_Button', n_clicks=0),
                    dcc.Graph(id='adj-matr'),
                    dcc.Graph(id='reordered_adj_matr')
                
                ])
        ])

tab_3_layout = html.Div([
            html.Div([
                html.Div([
                        html.Div(children = [html.H5('Starting time'),
                                 dcc.Dropdown(
                                    id='dyn-dropdown-time')], className = 'six columns'),
                        
                         html.Div([html.H5('Ending time'),
                             dcc.Dropdown(
                                id='dyn-dropdown-time-2')], className = 'six columns'
                            )
                 
                        
                    ], className = 'row'),
                             
                html.Div([
                    
                html.Div([html.H5('Select starting Log-weight'),
                        dcc.Input(id='dyn_edge_start', type='number',
                            #style={'width': '40%','float':'right', 'display': 'inline-block'}
                            )
                        ], className = 'six columns'),
                       

                    html.Div([html.H5('Select ending Log-weight'),
                                dcc.Input(id='dyn_edge_end', type='number',
                                    #style={'width': '40%', 'float' : 'right', 'display': 'inline-block'}
                                    )], className = 'six columns')
                            ], className = 'row'),

                html.Div([

                    html.Div([html.H5('Select first start node'),
                              dcc.Dropdown(id='dyn_start_node')
                              ], className = 'six columns'),
                    
                    html.Div([html.H5('Select last start node'),
                              dcc.Dropdown(id='dyn_start_end_node')
                              ], className = 'six columns')
                ], className= 'row'),
                
                html.Div([
                        html.Div(children = [html.H5('start node Dijkstra'),
                                 dcc.Dropdown(
                                    id='dyn-dropdown-Dijkstra')], className = 'six columns'),
                        
                         html.Div([html.H5('End node Dijkstra'),
                             dcc.Dropdown(
                                id='dyn-dropdown-Dijkstra-2')], className = 'six columns'
                            )
                 
                        
                    ], className = 'row'),

                html.Div([
                    html.Button('Plot', id='dyn_Button', n_clicks=0),
                    dcc.Graph(id='dyn_graph')]),
                    dcc.Graph(id='Dijkstra_dynamic')
                ])
        ])


tab_4_layout = html.Div([
            html.H5('Select timepoint'),
            dcc.Dropdown(id='dropdown-time_nl'),
            html.Button('Plot', id='nl_Button', n_clicks=0),
            dcc.Graph(id='nl_diagram')
        ])


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.H1(
            children='Visualization Tool - Group 8',
            style={
                    'textAlign': 'center'
                }
            ),
    html.Div(id='output-data-upload', style={'display':'none'}),
    dcc.Tabs(id="tabs-example", value='Home', children=[
        dcc.Tab(label='Home', value='Home', children=tab_1_layout),
        dcc.Tab(label='Aggregation', value='Aggr', children=tab_2_layout),
        dcc.Tab(label='Dynamic Graph Visualization', value='Dyn', children= tab_3_layout),
        dcc.Tab(label='Node link Diagram', value='Node link', children= tab_4_layout)
    ]),
    html.Div(id='tabs-content-example')
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' in filename:
            # Assume that the user uploaded an txt file
            df = sa.read_data(io.StringIO(decoded.decode('utf-8')))
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return  df


# Upload and store data
@app.callback(Output('output-data-upload', 'children'), [Input('upload-data', 'contents')], [State('upload-data', 'filename')])
def clean_data(contents, name):
    if contents is not None:
        # some expensive clean data step
        df = parse_contents(contents, name)
        # more generally, this line would be
        # json.dumps(cleaned_df)
        return df.to_json(date_format= "iso", orient="split")

    
# Show table on tab 1
@app.callback(
        Output('table', 'children'),
        [Input('output-data-upload', 'children')])
def plotTable(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return dt.DataTable(rows=data.to_dict('records'))


# Aggregation Visualization 
@app.callback(
        Output('aggr-slider-dropdown', 'options'),
        [Input('output-data-upload', 'children')])
def aggr_slider_1(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['time'].unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
        Output('aggr-slider-dropdown-2', 'options'),
        [Input('output-data-upload', 'children')])
def aggr_slider_2(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['time'].unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
    Output('adj-matr', 'figure'),
    [Input('aggr-slider-dropdown', 'value'), Input('aggr-slider-dropdown-2', 'value'),
     Input('output-data-upload','children'), Input('aggr_Button', 'n_clicks'),
     Input('aggr_scale', 'value')])
def update_adj(timestamp, timestamp2, df, n_clicks, scale):
    if df is not None and n_clicks > 0:
        data = pd.read_json(df, orient='split')[['time', 'start', 'target', 'logweight']]
        aggr_arr = sa.aggregate(data, timestamp, timestamp2, "sum")
        aggr_df = sa.array_to_df(aggr_arr)
        x_r, y_r = (aggr_df['start'].max(), aggr_df['target'].max())

        returnval = {
                'data':[
                    go.Scatter(
                        x = aggr_df['start'],
                        y = aggr_df['target'],
                        mode = 'markers',
                        marker = dict(
                                color = aggr_df['logweight'],
                                colorscale=scale,
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
                            'range' : [0,x_r],
                            'mirror' : 'ticks' 
                        },
                    yaxis={
                            'title':'target',
                            'showgrid':True,
                            'zeroline' : True,
                            'showline' : True,
                            'range' : [y_r,0]
                        }
                    )
                            
                }
        
        return returnval
    



@app.callback(
    Output('reordered_adj_matr', 'figure'),
    [Input('aggr-slider-dropdown', 'value'), Input('aggr-slider-dropdown-2', 'value'),
     Input('output-data-upload','children'), Input('aggr_Button', 'n_clicks'),
     Input('aggr_scale', 'value')])
def reorder_adj(timestamp, timestamp2, df, n_clicks, scale):
    if df is not None and n_clicks > 0:
        data = pd.read_json(df, orient='split')[['time', 'start', 'target', 'logweight']]
        aggr_df = dr.matr_re(data,10,timestamp,timestamp2)
        x_r, y_r = (aggr_df['start'].max(), aggr_df['target'].max())

        returnval = {
                'data':[
                    go.Scatter(
                        x = aggr_df['start'],
                        y = aggr_df['target'],
                        mode = 'markers',
                        marker = dict(
                                color = aggr_df['logweight'],
                                colorscale=scale,
                                reversescale = True,
                                showscale=True))
                    ],
                'layout':
                    go.Layout(
                    title='Reordered Adjacency Matrix Visualisation',
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
                            'range' : [y_r,0]
                        }
                    )
                            
                }
        
        return returnval


# Dynamic Graph visualization
@app.callback(
        Output('dyn_start_node', 'options'),
        [Input('output-data-upload', 'children')])
def dyn_dd_edge_1(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['start'].sort_values().unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
        Output('dyn_start_end_node', 'options'),
        [Input('output-data-upload', 'children')])
def dyn_dd_edge_2(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['start'].sort_values(ascending=False).unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
        Output('dyn-dropdown-time', 'options'),
        [Input('output-data-upload', 'children')])
def dyn_dd_time_1(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['time'].sort_values().unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
        Output('dyn-dropdown-time-2', 'options'),
        [Input('output-data-upload', 'children')])
def dyn_dd_time_2(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['time'].sort_values(ascending=False).unique()]
    else: return [{'label':1, 'value':1}]



@app.callback(Output('dyn_graph', 'figure'),
              [Input('dyn_Button', 'n_clicks'), Input('dyn-dropdown-time', 'value'),
               Input('dyn-dropdown-time-2', 'value'), Input('dyn_edge_start', 'value'),
               Input('dyn_edge_end', 'value'), Input('dyn_start_node', 'value'),
               Input('dyn_start_end_node', 'value'), Input('output-data-upload', 'children')])
def update_dyn(n_clicks, t_min, t_max, weight_start, weight_end, start_node, end_node, df):
    if (n_clicks > 0) and (df is not None):
        df = pd.read_json(df, orient='split')
        df = df.drop_duplicates(subset=['time', 'start', 'target'])
        df = df[(df['time'] >= t_min) & (df['time'] <= t_max) & (df['logweight'] >= weight_start) &
                (df['logweight'] <= weight_end) & (df['start'] >= start_node) & (df['start'] <= end_node)]
        df['cat_time'] = df['time'].astype('category')

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
                                 xaxis = {'showticklabels': False, 'type': 'category', 'tickangle': 45})                                           
                    }
        return returnval



@app.callback(
        Output('dyn-dropdown-Dijkstra', 'options'),
        [Input('output-data-upload', 'children')])
def dyn_dd_Dijkstra_start(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['start'].sort_values().unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
        Output('dyn-dropdown-Dijkstra-2', 'options'),
        [Input('output-data-upload', 'children')])
def dyn_dijkstra_time_2(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['target'].sort_values().unique()]
    else: return [{'label':1, 'value':1}]





@app.callback(Output('Dijkstra_dynamic', 'figure'),
              [Input('dyn_Button', 'n_clicks'), Input('dyn-dropdown-time', 'value'),
               Input('dyn-dropdown-time-2', 'value'), Input('dyn-dropdown-Dijkstra', 'value'),
               Input('dyn-dropdown-Dijkstra-2', 'value'), Input('output-data-upload', 'children')])
def update_dijkstra(n_clicks, t_min, t_max, start, target, df):
    if (n_clicks > 0) and (df is not None) and (t_min is not None):
        df = pd.read_json(df, orient='split')
        df = df.drop_duplicates(subset=['time', 'start', 'target'])
        df = df[(df['time'] >= t_min) & (df['time'] <= t_max)]
        df['cat_time'] = df['time'].astype('category')

        output = dijkstra.callDijkstra(start, target, df)
        print(output)
        lst_data = []
        for key in output.keys():
            trace_dict1 = {}
            x_list = []
            y_list = []
            x_list.append(key)
            y_list.append(output[key][0])
            for value in list(output[key])[1:-1]:
                x_list.append(key + 0.5)
                y_list.append(value)
                y_list.append(None)
                x_list.append(key)
                y_list.append(value)
                
            x_list.append(key + 0.5)
            y_list.append(output[key][-1])
            trace_dict1['x'] = x_list
            trace_dict1['y'] = y_list
            lst_data.append(trace_dict1)
        returnval = {
                    'data': [
                            go.Scatter(
                                x = trace['x'],
                                y = trace['y'],
                                connectgaps = False,
                                opacity= 0.5,
                                mode= 'lines'
                                ) for trace in lst_data
                        ],
                    'layout':
                         go.Layout(
                                 title='Shortest Path',
                                 showlegend = True,
                                 xaxis = {'showticklabels': True, 'type': 'category', 'tickangle': 45})                                           
                    }
        print(returnval)
        return returnval


@app.callback(
        Output('dropdown-time_nl', 'options'),
        [Input('output-data-upload', 'children')])
def nl_dd_time(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['time'].sort_values().unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
        Output('nl_diagram', 'figure'),
        [Input('output-data-upload', 'children'), Input('dropdown-time_nl', 'value'),
         Input('nl_Button', 'n_clicks'), Input('nl_diagram', 'clickData')])
def update_nl_diagram(df, time, n_clicks, clickdata):
    if (n_clicks >0) and (df is not None):
        df = pd.read_json(df, orient='split')
        if clickdata is not None:
            textval = str(clickdata['points'][0]['text'])
            return nl.nodelink(time, df, textval)
        return nl.nodelink(time, df)


if __name__ == '__main__':
    app.run_server(debug=True)
