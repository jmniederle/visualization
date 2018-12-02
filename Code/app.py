<<<<<<< HEAD
# Neccesary imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.dashboard_objs as dashboard
import IPython.display
from IPython.display import Image
import plotly.plotly as py

my_dboard = dashboard.Dashboard()
my_dboard.get_preview()

box_1 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': 'PlotBot:1296',
    'title': 'scatter-for-dashboard'
}

box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': 'PlotBot:1298',
    'title': 'pie-for-dashboard'
}
 
box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': 'PlotBot:1342',
    'title': 'box-for-dashboard',
    'shareKey':'uVoeGB1i8Xf4fk0b57sT2l'}


py.dashboard_ops.upload(my_dboard, 'My First Dashboard with Python')


# Code for a graph
##################################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center'
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center'
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ]
        }
    )
])

# Code for markdown
##################################
#app.layout = html.Div([
#    html.Label('Dropdown'),
#    dcc.Dropdown(
#        options=[
#            {'label': 'New York City', 'value': 'NYC'},
#            {'label': u'Montréal', 'value': 'MTL'},
#            {'label': 'San Francisco', 'value': 'SF'}
#        ],
#        value='MTL'
#    ),
#
#    html.Label('Multi-Select Dropdown'),
#    dcc.Dropdown(
#        options=[
#            {'label': 'New York City', 'value': 'NYC'},
#            {'label': u'Montréal', 'value': 'MTL'},
#            {'label': 'San Francisco', 'value': 'SF'}
#        ],
#        value=['MTL', 'SF'],
#        multi=True
#    ),
#
#    html.Label('Radio Items'),
#    dcc.RadioItems(
#        options=[
#            {'label': 'New York City', 'value': 'NYC'},
#            {'label': u'Montréal', 'value': 'MTL'},
#            {'label': 'San Francisco', 'value': 'SF'}
#        ],
#        value='MTL'
#    ),
#
#    html.Label('Checkboxes'),
#    dcc.Checklist(
#        options=[
#            {'label': 'New York City', 'value': 'NYC'},
#            {'label': u'Montréal', 'value': 'MTL'},
#            {'label': 'San Francisco', 'value': 'SF'}
#        ],
#        values=['MTL', 'SF']
#    ),
#
#    html.Label('Text Input'),
#    dcc.Input(value='MTL', type='text'),
#
#    html.Label('Slider'),
#    dcc.Slider(
#        min=0,
#        max=9,
#        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
#        value=5,
#    ),
#], style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)
=======
import base64
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import StorageAggregation as sa

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = True

app.layout = html.Div([
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
    html.Div(id='output-data-upload')])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'txt' in filename:
            array, df = sa.read_data(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        dt.DataTable(rows=df.to_dict('records')),
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        children = [
            parse_contents(contents, filename)]
        return children



if __name__ == '__main__':
    app.run_server(debug=True)
>>>>>>> be5830219abea2e7c3857a6b4ba37af8d36c6b50
