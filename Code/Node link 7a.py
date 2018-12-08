from __future__ import division
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

def read_data(filename):

    df = pd.read_csv(filename, sep = ' ', index_col = False)

    data = np.zeros((1232, 981, 983), np.int64)

    for row in df.iterrows():
        time = row[1][0]
        start = row[1][1]
        target = row[1][2]
        weight = row[1][3]

        data[time][start][target] = weight

    return data

data = read_data('profile_semantic_trafo_final.txt')

# Making a dataframe from the first timeslot
df = pd.DataFrame(data[1])
# Dropping all rows and columns with only 0 values (these are not neccesary in a node link diagram)
df = df.loc[:, (df != 0).any(axis=0)]
df = df[(df.T != 0).any()]


G = nx.generators.directed.random_k_out_graph(10, 3, 0.5)
pos = nx.layout.spring_layout(G)

node_sizes = [3 + 10 * i for i in range(len(G))]
M = G.number_of_edges()
edge_colors = range(2, M + 2)
edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                               arrowsize=10, edge_color=edge_colors,
                               edge_cmap=plt.cm.Blues, width=2)
# set alpha value for each edge
for i in range(M):
    edges[i].set_alpha(edge_alphas[i])

pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
pc.set_array(edge_colors)
plt.colorbar(pc)

ax = plt.gca()
ax.set_axis_off()
plt.show()










