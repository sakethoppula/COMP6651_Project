import random
import networkx as nx

from itertools import combinations

def triangle_free_graph(total_nodes):
    """Construct a triangle free graph."""
    nodes = range(total_nodes)
    g = nx.Graph()
    g.add_nodes_from(nodes)
    edge_candidates = list(combinations(nodes, 2))
    random.shuffle(edge_candidates)
    for (u, v) in edge_candidates:
        if not set(n for n in g.neighbors(u)) & set(n for n in g.neighbors(v)):
            g.add_edge(u, v)
    return g

g = triangle_free_graph(5)
print(g)
print(g.nodes())
print(g.edges())
print(nx.triangles(g))

#0,1,2,3,4

#0-1,0-2,1-4,2-3,3-4
