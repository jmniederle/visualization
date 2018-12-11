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


if __name__ == '__main__':
    app.run_server(debug=True)
'''