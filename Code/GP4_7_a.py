# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:12:25 2018

@author: 20175878
"""
import pandas as pd
import networkx as nx
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

final = pd.read_csv('profile_semantic_trafo_final.txt', delimiter='\s')

dct = {}

for row in final.iterrows():
    if (row[1]['time']) not in dct:
        dct[row[1]['time']] = [[row[1]['start'], row[1]['target'], row[1]['weight']]]
    else:
        dct[row[1]['time']].append([row[1]['start'], row[1]['target'], row[1]['weight']])
        
for timestamp in dct:
    for tpl in dct[timestamp]:
      tpl[2] = np.log(tpl[2])


def draw_simple(timestamp):
    G = nx.DiGraph()
    for node in dct[timestamp]:
        G.add_edge(node[0], node[1], weight=node[2])
        
    nx.draw(G, with_labels=True, node_size=100, node_color="skyblue", pos=nx.spring_layout(G, scale = 3))
    #nx.draw(G, with_labels=True, node_size=100, node_color="skyblue", pos=nx.spring_layout(G, scale = 3), arrowstyle='fancy')
def draw_weighted(timestamp):
    G = nx.DiGraph()
    for node in dct[timestamp]:
        G.add_edge(node[0], node[1], weight=node[2])
        
#    nx.draw(G, with_labels=True, node_size=100, node_color="skyblue", pos=nx.spring_layout(G, scale = 3))
    nx.draw(G, with_labels=True, node_size=100, node_color="skyblue", pos=nx.spring_layout(G, scale = 3), arrowstyle='fancy')

draw_simple(48)
draw_weighted(48)

def get_nodes_edges_weights(timestamp):
    from_list = []
    for i in dct[timestamp]:
        from_list.append([i[0],i[1], i[2]])
    return(from_list)
A = get_nodes_edges_weights(48)
A
def make_G(timestamp):
    G = nx.Graph()
    edges = get_nodes_edges_weights(timestamp)
    for i in edges:
        G.add_edge(i[0], i[1], weight = i[2])
    pos = nx.layout.spring_layout(G)
    return(G, pos)
    
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

G, pos = make_G(48)
pos
G.node[edge[0]][pos[0]]
for edge in G.edges():
    x0, y0 = G.node[edge[0]][pos[G.node]]
    x1, y1 = G.node[edge[1]][pos[G.node]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])
#from storage_aggr import read_data
#
#array, df = read_data('profile_semantic_trafo_final.txt')

