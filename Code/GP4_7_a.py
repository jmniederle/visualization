# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:12:25 2018

@author: 20175878
"""
import pandas as pd
import networkx as nx
import numpy as np

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

# DRAW SIMPLE GRAPH, USE THIS ONE FOR ASSIGNMENT 4 EXERCISE 7A
def draw_simple(timestamp):
    G = nx.Graph()
    for node in dct[timestamp]:
        G.add_edge(node[0], node[1])
        
    nx.draw(G, with_labels=True, node_size=500, node_color="skyblue", pos=nx.spring_layout(G, scale = 3))
    
# DRAW WEIGHTER GRAPH, USE THIS ONE FOR ASSIGNMENT 4 EXERCISE 7B
def draw_weighted(timestamp):
    G = nx.DiGraph()
    for node in dct[timestamp]:
        G.add_edge(node[0], node[1], weight=node[2])
        edges = G.edges()
        weights = [G[u][v]['weight']*0.3 for u,v in edges]
        
    nx.draw(G, with_labels=True, node_size=500, node_color="skyblue", pos=nx.spring_layout(G, scale = 3), arrowstyle='fancy', width=weights)

# CALL FUNCITON AND INSERT TIMESTAMP
draw_simple(TIMESTAMP) OR draw_weighted(TIMESTAMP)