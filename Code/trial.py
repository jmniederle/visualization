num_nodes = 2000
edge = df['itemset'][:num_nodes]
#create graph G
G = nx.Graph()
#G.add_nodes_from(node)
G.add_edges_from(edge)
#get a x,y position for each node
pos = nx.layout.spring_layout(G)