# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:12:25 2018

@author: 20175878
"""

import pandas as pd
import networkx as nx
import numpy as np

final = pd.read_csv('C:/Users/20175878/Documents/GitHub/visualization/Dataset/profile_semantic_trafo_final.txt', delimiter='\s')

dct = {}

for row in final.iterrows():
    if (row[1]['time']) not in dct:
        dct[row[1]['time']] = [[row[1]['start'], row[1]['target'], row[1]['weight']]]
    else:
        dct[row[1]['time']].append([row[1]['start'], row[1]['target'], row[1]['weight']])
        
for timestamp in dct:
    for tpl in dct[timestamp]:
      tpl[2] = np.log(tpl[2])

G = nx.DiGraph()
    
for node in dct[48]:
    G.add_edge(node[0], node[1], weight=node[2])
    
nx.draw(G, with_labels=True, node_size=100, node_color="skyblue", pos=nx.spring_layout(G))