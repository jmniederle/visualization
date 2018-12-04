# -*- coding: utf-8 -*-

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(
            children='Visualization Tool - Group 8',
            style={
                    'textAlign': 'center'
                }
            ),
    dcc.Tabs(id="tabs-example", value='Home', children=[
        dcc.Tab(label='Home', value='Home'),
        dcc.Tab(label='Dynamic Graph Visualization', value='Visualization1'),
        dcc.Tab(label='Shortest path algorithm', value='Dijkstra'),
        dcc.Tab(label='Aggregation', value='Aggregation')
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
    
def render_content(tab):
    if tab == 'Home':
        return html.Div([
            html.H1('Insert Text')

        ])
    elif tab == 'Visualization1':
        return html.Div([
            html.H1('Insert Text')
        ])
    elif tab == 'Dijkstra':
        return html.Div([
                html.H1('Insert text')])
    elif tab == 'Aggregation':
        return html.Div([
                html.H1('Insert text')])


if __name__ == '__main__':
    app.run_server(debug=True)
