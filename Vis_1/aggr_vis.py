# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


from storage_aggr import aggregate, array_to_df , read_data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = read_data('profile_semantic_trafo_final.txt')



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H4('Starting time'),
            dcc.Dropdown(
                id='time-slider',
                options=[{'label': i, 'value': i} for i in df['time'].unique()],
                value=1),
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.H4('End time'),
            dcc.Dropdown(
                id='time-slider2',
                options=[{'label': i, 'value': i} for i in df['time'].unique()],
                value=1),
        ],
        style={'width': '48%', 'float' : 'right', 'display': 'inline-block', 'vertical-align': 'top'}),
        
    ]),
    dcc.Graph(
        id='adj-matr' 
        )

])


@app.callback(
    dash.dependencies.Output('adj-matr', 'figure'),
    [dash.dependencies.Input('time-slider', 'value'), dash.dependencies.Input('time-slider2', 'value')])
def update_dy(timestamp, timestamp2): # inp_df toevoegen
    df = read_data('profile_semantic_trafo_final.txt')[['time', 'start', 'target', 'logweight']]
    aggr_arr = aggregate(df, timestamp, timestamp2, "sum")
    aggr_df = array_to_df(aggr_arr)
    #x_r, y_r = (aggr_df['start'].max(), aggr_df['target'].max())
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
                        'mirror' : 'ticks' 
                    },
                yaxis={
                        'title':'target',
                        'showgrid':True,
                        'zeroline' : True,
                        'showline' : True
                    }
                )
                        
            }
    
    return returnval


if __name__ == '__main__':
    app.run_server(debug=True)
