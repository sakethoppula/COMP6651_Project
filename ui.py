import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pyvis.network import Network

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Interactive Graph Visualization'),
    dcc.Input(id='node-input', type='text', placeholder='Enter node label'),
    html.Button(id='add-node-button', n_clicks=0, children='Add Node'),
    dcc.Dropdown(id='edge-start-dropdown', placeholder='Select start node'),
    dcc.Dropdown(id='edge-end-dropdown', placeholder='Select end node'),
    html.Button(id='add-edge-button', n_clicks=0, children='Add Edge'),
    dcc.Graph(id='graph-display')
])

# Create an empty PyVis network
network = Network()

# Define a callback function for adding nodes
@app.callback(Output('graph-display', 'figure'),
              Input('add-node-button', 'n_clicks'),
              State('node-input', 'value'))
def add_node(n_clicks, node_label):
    if node_label:
        # Add the node to the network
        network.add_node(node_label)

    # Update the graph display
    fig = network.get_network()
    return {'data': fig['data'], 'layout': fig['options']}

# Define a callback function for adding edges
@app.callback(Output('graph-display', 'figure'),
              Input('add-edge-button', 'n_clicks'),
              State('edge-start-dropdown', 'value'),
              State('edge-end-dropdown', 'value'))
def add_edge(n_clicks, start_node, end_node):
    if start_node and end_node:
        # Add the edge to the network
        network.add_edge(start_node, end_node)

    # Update the dropdown options
    node_labels = network.nodes
    fig = network.get_network()
    return {'data': fig['data'], 'layout': fig['options']}

# Define a callback function for updating the dropdown options
@app.callback(Output('edge-start-dropdown', 'options'),
              Output('edge-end-dropdown', 'options'),
              Input('graph-display', 'clickData'))
def update_dropdowns(click_data):
    if click_data:
        # Get the node that was clicked on
        node_label = click_data['points'][0]['label']

        # Update the dropdown options
        node_labels = network.nodes
        node_labels.remove(node_label)
        dropdown_options = [{'label': label, 'value': label} for label in node_labels]
        return dropdown_options, dropdown_options
    else:
        return [], []

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
