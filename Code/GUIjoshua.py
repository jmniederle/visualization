import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

app=dash.Dash()


app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar'}
                ],
                'layout': {
                    'title': 'Dash Data Visualization',
                    'height':500
                    }
                }
            ),
        ],
        style={'width': '20%', 'display': 'inline-block'}
        ),

    html.Div([
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
                ],
            value=['MTL', 'SF'],
            multi=True
        ),

        dcc.Graph(
            id='example-graph3',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar'}
                ],
                'layout': {
                    'title': 'Dash Data Visualization',
                    'height':500
                    }
                }
            )
        ],
        style={'width': '60%', 'display': 'inline-block'}
        ),

    html.Div([
        dcc.Graph(
            id='example-graph4',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar'}
                ],  
                'layout': {
                    'title': 'Dash Data Visualization',
                    'height':500
                    }
                }
            )
        ],
        style={'width': '20%', 'display': 'inline-block', 'float': 'right'},
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
