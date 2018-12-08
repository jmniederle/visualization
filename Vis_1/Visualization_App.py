# -*- coding: utf-8 -*-

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
                    html.Button('Plot', id='aggr_Button', n_clicks=0),
                    dcc.Graph(
                        id='adj-matr' 
                        )
                
                ])
        ])

tab_3_layout = html.Div([
            html.H1('Insert Dynamic Graph')
        ])

tab_4_layout = html.Div([
            html.H1('Insert Dijkstra')
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
        dcc.Tab(label='Shortest path algorithm', value='Short', children= tab_4_layout)
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
        Output('aggr-slider-dropdown','options'),
        [Input('output-data-upload', 'children')])
def aggr_slider_1(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['time'].unique()]
    else: return [{'label':1, 'value':1}]


@app.callback(
        Output('aggr-slider-dropdown-2','options'),
        [Input('output-data-upload', 'children')])
def aggr_slider_2(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return [{'label': i, 'value': i} for i in data['time'].unique()]
    else: return [{'label':1, 'value':1}]

        


@app.callback(
    Output('adj-matr', 'figure'),
    [Input('aggr-slider-dropdown', 'value'), Input('aggr-slider-dropdown-2', 'value'),
     Input('output-data-upload','children'), Input('aggr_Button', 'n_clicks')])
def update_dy(timestamp, timestamp2, df, n_clicks):
    if df is not None and n_clicks > 0:
        data = pd.read_json(df, orient='split')[['time', 'start', 'target', 'logweight']]
        aggr_arr = sa.aggregate(data, timestamp, timestamp2, "sum")
        aggr_df = sa.array_to_df(aggr_arr)
        x_r, y_r = (aggr_df['start'].max(), aggr_df['target'].max())
        #df = inp_df[inp_df['time']==timestamp]
        #print(df.describe())
        returnval = {
                'data':[
                    go.Scatter(
                        x = aggr_df['start'],
                        y = aggr_df['target'],
                        mode = 'markers',
                        marker = dict(
                                color = aggr_df['logweight'],
                                colorscale='Viridis',
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


if __name__ == '__main__':
    app.run_server(debug=True)
