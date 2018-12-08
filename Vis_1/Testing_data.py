import plotly.graph_objs as go
#import pandas as pd
import storage_aggr as sa
import time
import dash
import dash_html_components as html
import dash_core_components as dcc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = sa.read_data('profile_semantic_trafo_final.txt')
df = df.drop_duplicates(subset=['time', 'start', 'target'])
#dyn_graph_df = df.drop_duplicates(subset=['time', 'start', 'target'])

'''
lst =[]
for row in dyn_graph_df.iterrows():
    lst.append([row[1]['time'], row[1]['start'], (row[1]['time'] + 0.5), row[1]['target'], row[1]['logweight']])

dyn_graph_df =pd.DataFrame(lst)
'''




start = time.time()
lst2 = []
for edge in range(639): # highest count of edges for time
    print(edge)
    trace_dict = {}
    x_trace = []
    y_trace = []
    for timestamp in df['time'].unique():
        df1 = df[df['time'] == timestamp]
        try:
            row = df1.iloc[edge]
            x_trace.append(row['time'])
            x_trace.append(row['time'] + 0.5)
            y_trace.append(row['start'])
            y_trace.append(row['target'])
        except: 
            pass
    trace_dict['x'] = x_trace
    trace_dict['y'] = y_trace
    lst2.append(trace_dict)
print(start - time.time()) 


app.layout = html.Div(dcc.Graph(id='dyn_graph',
                                figure={
                                        'data': [
                                                go.Scatter(
                                                    x = trace['x'],
                                                    y = trace['y'],
                                                    connectgaps = False,
                                                    mode= 'lines'
                                                    ) for trace in lst2
                                            ]
                                        }
    ))


if __name__ == '__main__':
    app.run_server(debug=True)



#df['time'] = df['time'].astype('category')
#df['time'].describe()