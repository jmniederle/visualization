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

markdown_text= '''
Welcome to our Visualization tool!
'''

app.layout = html.Div(children=[
        html.H1(children="Visualization Group 8", style={'textAlign':'center'}),
        dcc.Markdown(markdown_text),
        html.Div([
                
                # Column 1
                html.Div(children=[
                        html.H3('Input'),
                        html.H5('File-type', style={'backgroundColor': '#FFFFFF'}),
                        html.Hr(),
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
                                'borderRadius': '1px',
                                'textAlign': 'center',
                                'backgroundColor': '#FFFFFF'
                                },
                                multiple=False)
                                             
                ], style={'width':'20%', 'display':'inline-block', 'margin':'50px', 'vertical-align':'top', 'backgroundColor':'#FFFFFF'}),


                # Column 2
                html.Div([
                        html.H3('Visualization'),
                        html.Hr(),
                        html.Div(id='output-data-upload')
                ], style={'width':'40%', 'display':'inline-block', 'vertical-align':'top', 'backgroundColor':'#FFFFFF'}),


                # Column 3
                html.Div([
                        html.H3('Output'),
                ], style={'width':'20%', 'display':'inline-block', 'margin':'50px', 'vertical-align':'top','backgroundColor':'#FFFFFF'})


        ], className = 'row')
])#, #style={'background-image':'url(https://image.freepik.com/free-vector/abstract-geometric-pattern-background_1319-242.jpg)'})
  


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        array, df = sa.read_data(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ], style={'backgroundColor': '#FFFFFF'})

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
