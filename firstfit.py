import networkx as nx

def first_fit(graph):
    # Initialize an empty list of colors
    colors = []

    # Assign each vertex the smallest available color
    for vertex in graph.nodes():
        # Find the smallest available color
        available_colors = set(range(len(colors) + 1))
        for neighbor in graph.neighbors(vertex):
            if graph.nodes[neighbor]['color'] in available_colors:
                available_colors.remove(graph.nodes[neighbor]['color'])

        # Assign the vertex the smallest available color
        if len(available_colors) > 0:
            color = min(available_colors)
        else:
            color = len(colors)
            colors.append(color)
        print (color)
        graph.nodes[vertex]['color'] = color

    return colors

# Example usage:
G = nx.Graph()
G.add_edges_from([(1,6),(1,9),(2,8),(3,6), (3,7), (4,8), (4,9), (5,9)])

# Add color attribute to each node
for node in G.nodes():
    G.nodes[node]['color'] = 0

# for node in G.nodes():
#     print(G.nodes[node]['color'])

colors = first_fit(G)
print(colors) 
