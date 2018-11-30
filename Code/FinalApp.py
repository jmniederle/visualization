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
        
            html.Div([html.H1('Visualization Group 8', style={'textAlign': 'center', 'borderStyle': 'dashed'})]),
        
            html.Div(
                className="row",
                children=[               
            # Start Column 1
            html.Div(className= "six columns",
                     children=[
                    html.H2('Hallo')], 
                    style= {'width':'100%', 'borderStyle': 'dashed'}), 
        
            
            # Start middle column
            html.Div(
                    className= "six-columns",
                    children=[
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
                                'borderWidth': '1.5px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '0px',
                                'backgroundColor': '#FFFFFF'
                                },
                                multiple=False),
                        html.Div(id='output-data-upload')
                    ]
                ),
                
            
            # Start Column 3
            html.Div(
                    className= "six columns",
                    children=[html.H3('Style')]
                     )
        ])
])



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
