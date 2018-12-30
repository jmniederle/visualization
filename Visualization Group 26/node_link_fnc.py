
import plotly.graph_objs as go
import networkx as nx


def nodelink(timepoint, df, click_text=None):
    dct = {}
    
    for row in df.iterrows():
        if (row[1]['time']) not in dct:
            dct[row[1]['time']] = [[row[1]['start'], row[1]['target'], row[1]['logweight']]]
        else:
            dct[row[1]['time']].append([row[1]['start'], row[1]['target'], row[1]['logweight']])
            
    
    
    
    G = nx.DiGraph()
    for node in dct[timepoint]:
        G.add_edge(node[0], node[1], weight=node[2])
        
    
    pos = nx.spring_layout(G, scale = 3)
        
    
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1,color='#888'),
        hoverinfo='none',
        mode='lines')
    
    for edge in G.edges():
        x0 = pos[edge[0]][0]
        y0 = pos[edge[0]][1]
        x1 = pos[edge[1]][0]
        y1 = pos[edge[1]][1] 
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])    
    
    
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            color='#1f77b4',
            size=10))

    
    for node in G.nodes():
        x = pos[node][0]
        y = pos[node][1]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([int(node)])
    
    if click_text in node_trace['text']:
        idx = node_trace['text'].index(click_text)
        marked_trace = go.Scatter(x=[node_trace['x'][idx]], y=[node_trace['y'][idx]], text=[click_text],
                                    mode='markers',
                                    hoverinfo='text',
                                    marker=dict(
                                        color='RGB(255,40,0)',
                                        size=20))
    else:
        marked_trace = go.Scatter()
    fig = go.Figure(data=[edge_trace, node_trace, marked_trace],
                 layout=go.Layout(
                    title='Node link diagram for time {}'.format(timepoint),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    return fig