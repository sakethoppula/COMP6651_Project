import numpy as np
import random




def filter_colors(colors, lis):
    for i in lis:
        # print(i)
        if i in colors:
            colors.remove(i)
    return colors

def competitive_ratio(number_of_colors_used, k):
    return float(number_of_colors_used) / float(k)

# Assigns colors (starting from 0) to all
# vertices and prints the assignment of colors
def firstfit(adj, V):
    partial_graph = []
    vertex_colors = dict()
    for i in range(V):
        vertex_colors[i] = -1

    # result = [-1] * V
    Col = list(np.arange(0,V))
    Col = sorted(Col, reverse=True)
    colors = Col.copy()

    # Assign colors to remaining V-1 vertices
    for u in range(0, V):
        partial_graph.append(u)
        lis = []
        for i in adj[u]:
            if i in partial_graph:
                lis.append(vertex_colors[i])
        result = filter_colors(colors, lis)
        vertex_colors[u] = result.pop()
        colors = Col.copy()
    return len(set(list(vertex_colors.values())))


def generate_k_colorable_graph(n, k, p):
    # Step 1: Partition the vertices into k disjoint sets
    partition = [set() for _ in range(k)]
    x = np.random.randint(0, 10)
    for i in range(n):
        partition[(i+x) % k].add(i+1)

    # Step 2: Generate edges between vertices in different sets with probability p
    edges = set()
    for i in range(0, n):
        for j in range(i, n):
            if i in partition[j % k] or j in partition[i % k]:
                continue # Skip if i and j are in the same set
            if random.random() < p:
                edges.add((i, j))

    # Return the graph as an adjacency list
    graph = [[] for i in range(1, n+1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph



# Driver Code
if __name__ == '__main__':
    random.seed(30)
    for k in [2, 3, 4]:
        print(f"For k = {k}: ")
        lst1, lst2, lst3 = [], [], []
        for n in [50, 100, 200, 400, 600, 800, 1000, 1200]:
            lst = []
            for N in range(100):
                p = random.random()
                g1 = generate_k_colorable_graph(n, k, p)
                colors_used = firstfit(g1, n)
                lst.append(competitive_ratio(colors_used, k))
            if n % 2 == 0:
                print(f"For {n} vertices, avg. CR - {round(sum(lst) / len(lst), 2)}")