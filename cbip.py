class CBIP:
    def __init__(self, k):
        self.k = k
        self.color_map = {}
        self.independent_sets = [[] for _ in range(k)]
    
    def color_vertex(self, v):
        # Find the independent set that v belongs to
        hv = self._find_hv(v)
        
        # Find the smallest unused color
        color = self._find_color(hv)
        
        # Color v with the smallest unused color
        self.color_map[v] = color
        
        # Add v to its independent set
        hv.append(v)
    
    def _find_hv(self, v):
        for hv in self.independent_sets:
            if all(self._is_independent(v, u) for u in hv):
                return hv
        raise ValueError("No independent set found for vertex")
    
    def _is_independent(self, u, v):
        return u not in self.color_map or self.color_map[u] != self.color_map[v]
    
    def _find_color(self, hv):
        used_colors = {self.color_map[v] for v in self.color_map if v not in hv}
        for color in range(self.k):
            if color not in used_colors:
                return color
        raise ValueError("No color available for vertex")


# Example usage
if __name__ == '__main__':
    # Create an instance of CBIP with k=3
    cbip = CBIP(3)
    
    # Define an example graph as an adjacency list
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2],
        4: [2, 5],
        5: [4],
        6: []
    }
    
    # Color the vertices of the graph using CBIP
    for v in graph:
        cbip.color_vertex(v)
    
    # Print the final coloring of the graph
    print(cbip.color_map)
