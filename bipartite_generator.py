import random

def generate_bipartite_graph(m, n, p):
    # m nodes in the left partition, n nodes in the right partition
    # p is the probability of a left node being connected to a right node
    left_partition = list(range(0, m))
    right_partition = list(range(m, m+n))
    edges = []
    for u in left_partition:
        for v in right_partition:
            if random.random() < p:
                edges.append((u, v))
    return edges

nod = ''
ed = generate_bipartite_graph(2, 3, 1)
for a in range(0,5):
    nod = nod + (str(a)+',')

print(nod)
edg = ''
for a in ed:
    edg = edg + (str(a[0])+'-'+str(a[1])+",")
print(edg)