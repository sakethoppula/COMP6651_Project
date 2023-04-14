import dash
from dash import dcc
from dash import html
import networkx as nx
import pandas as pd
import plotly.graph_objs as go

# Create a Dash app
app = dash.Dash(__name__)

# Create a NetworkX graph
G = nx.Graph()

# Define the app layout
app.layout = html.Div([
    html.H1('GRAPH GENERATOR COMP6551'),
    dcc.Input(id='input-nodes', type='text', placeholder='Enter node IDs separated by commas'),
    dcc.Input(id='input-edges', type='text', placeholder='Enter edges separated by commas'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    dcc.Graph(id='graph')
])

def Firstfit(graph):
    """
    Assigns colors to vertices in a bipartite graph using the First Fit algorithm.
    """
    # Partition the vertices of the graph into two sets
    set_A = set()
    set_B = set()
    for vertex in graph:
        if vertex % 2 == 0:
            set_A.add(vertex)
        else:
            set_B.add(vertex)
   
    # Initialize an empty color set and an empty dictionary to keep track of the colors assigned to each vertex
    colors = set()
    color_dict = {}
   
    # Assign colors to vertices in set A
    for vertex in set_A:
        # Find the first available color
        available_colors = colors.copy()
        for neighbor in graph[vertex]:
            if neighbor in set_B and neighbor in color_dict:
                available_colors.discard(color_dict[neighbor])
        if available_colors:
            color = min(available_colors)
        else:
            color = len(colors) + 1
            colors.add(color)
        color_dict[vertex] = color
   
    # Assign colors to vertices in set B
    for vertex in set_B:
        # Find the first available color
        available_colors = colors.copy()
        for neighbor in graph[vertex]:
            if neighbor in set_A and neighbor in color_dict:
                available_colors.discard(color_dict[neighbor])
        if available_colors:
            color = min(available_colors)
        else:
            color = len(colors) + 1
            colors.add(color)
        color_dict[vertex] = color
   
    # Return the list of colors assigned to each vertex
    return color_dict



# Define a callback to update the graph based on user input
@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input-nodes', 'value'),
     dash.dependencies.State('input-edges', 'value')]
)
def update_graph(n_clicks, input_nodes, input_edges):
    if n_clicks > 0:
        # Convert the user input into lists of nodes and edges
        nodes = [int(x.strip()) for x in input_nodes.split(',')]
        edges = [(int(x.strip().split('-')[0]), int(x.strip().split('-')[1])) for x in input_edges.split(',')]
        
        # Add the nodes and edges to the graph
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        print(G.nodes())
        print(G.edges())
        output = Firstfit(G)
        print(output)
        # Create a Plotly figure from the NetworkX graph
        pos = nx.spring_layout(G)
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5,color='#888'),
            hoverinfo='none',
            mode='lines')
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        # Set the colors and text for each node
        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append('Node ' + str(node) + ' has ' + str(len(adjacencies[1])) + ' connections' + " with color: " + str(output[node]))
            
        node_trace['marker']['color'] = node_adjacencies
        node_trace['text'] = node_text
        
        # Create the Plotly figure
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='<br>Network graph made with Python',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            annotations=[dict(
                            text="GRAPH",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 )],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                   )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
