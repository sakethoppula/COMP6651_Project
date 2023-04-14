import networkx as nx
import matplotlib.pyplot as plt
# G = nx.Graph() 
# E = [('A', 'B', 2), ('A', 'C', 1), ('B', 'D', 5), ('B', 'E', 3), ('C', 'E', 2)]
# G.add_weighted_edges_from(E)
# pos=nx.spring_layout(G)


import random
import networkx as nx

def generate_random_graph(n, p):
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                G.add_edge(i, j)
    return G
G = generate_random_graph(6, 0.1)
pos=nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold')
edge_weight = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
plt.show()