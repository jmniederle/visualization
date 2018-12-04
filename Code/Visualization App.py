# -*- coding: utf-8 -*-

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import pandas as pd
import base64
import io
import StorageAggregation as sa

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

tab_1_layout = html.Div([
            html.H1('Insert Text'),
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
            html.H1('Insert Dynamic Graph'),
        ])

tab_3_layout = html.Div([
            html.H1('Insert Dijkstra')
        ])

tab_4_layout = html.Div([
            html.H1('Insert Aggregation')
        ])


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True

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
        dcc.Tab(label='Dynamic Graph Visualization', value='Visualization1', children=tab_2_layout),
        dcc.Tab(label='Shortest path algorithm', value='Dijkstra', children= tab_3_layout),
        dcc.Tab(label='Aggregation', value='Aggregation', children= tab_4_layout)
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
            array, df = sa.read_data(io.StringIO(decoded.decode('utf-8')))
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return (array, df)


@app.callback(Output('output-data-upload', 'children'), [Input('upload-data', 'contents')], [State('upload-data', 'filename')])
def clean_data(contents, name):
    if contents is not None:
        # some expensive clean data step
        array, df = parse_contents(contents, name)
        # more generally, this line would be
        # json.dumps(cleaned_df)
        return df.to_json(date_format= "iso", orient="split")

    

@app.callback(
        Output('table', 'children'),
        [Input('output-data-upload', 'children')])
def plotTable(df):
    if df is not None:
        data = pd.read_json(df, orient='split')
        return dt.DataTable(rows=data.to_dict('records'))
 
if __name__ == '__main__':
    app.run_server(debug=True)





