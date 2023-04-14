import sys
import copy

"""
First off a node class. For the purposes of this script we will have a graph
class as well which is an aggregation of nodes in addition to a method for
generating an HTML document.
"""
class node:
    def __init__(self):
        # by default the node is not connected to anything so we set the connections map to an empty dictionary
        self.connections = {}

    def connect(self, n, weight=1):
        # By making connections a dictionary instead of a list we are not limited to consecutive integers starting at 0
        # As such are data structure will be able to handle sparse connectivity well as non-connections are not stored.
        self.connections[n] = weight

    def disconnect(self, n):
        # We want to be able to remove a connection and as non-connections are not stored we need to remove the value
        # from the designated index, if it exists. We use a try catch to avoid any complexity introduced by comparing
        # with non-values
        try:
            del self.connections[n]
        except KeyError:
            # Remove the errors from log as nothing really went wrong.
            sys.exc_clear()

"""
grey takes a number [0:254] and returns a shade of grey.
"""
def grey(n):
    # we are interested in the string representation of a number in hex to be used for r,g and b.
    # multiplaction of strings is repition, i.e. "a"*3 = "aaa" and the hex call returns a string "...xSOMENUMBER"
    return ("#" + hex(n).split("x")[1] * 3)

"""
palet takes a start and end color as well as a number of steps and returns an array of colors
"""
def palet(n, start, end):
    col = lambda x: "#" + "".join(["0" * (2 - len(hex(k).split("x")[1])) + hex(k).split("x")[1] for k in x])
    ret = []
    ret.append(col(start))
    d = [(end[k] - start[k]) / n for k in range(0, 3)]
    temp = start
    for k in range(0, n - 2):
        temp = [temp[k] + d[k] for k in range(0, 3)]
        ret.append(col(temp))
    ret.append(col(end))
    return ret

"""
The graph class is the main visible interface for future use. It is intended to provide a straight forward interface
for adding nodes and edges to a graph which can be easily visualized in an HTML document.
"""
class graph:
    def __init__(self):
        # The graph is naive to the names of the nodes, and the nodes of the graph are stored as a list.
        self.nodes = []
        # To enable removal of nodes on the fly the active variable is used to limit signal propagation from nodes
        # where active = False
        self.active = []

    def visGraph(self):
        # This method produces a graph color coated by connectivity.
        groups = self.subnets()
        groupsReshaped = {}
        for n, k in enumerate(groups):
            for k2 in k:
                groupsReshaped[k2] = n
        p = palet(len(groups), [250, 0, 0], [0, 0, 250])
        nodes = "[" + ",".join(
            ["{id: " + str(n) + ", color: '" + p[groupsReshaped[n]] + "' ,label: 'Node " + str(n) + "'}" for n, k in
             enumerate(self.nodes)]) + "]"
        edges = []
        for n, k in enumerate(self.nodes):
            edges = edges + ["{from: " + str(n) + ", to: " + str(k2) + "}" for k2 in k.connections]
        edges = "[" + ",".join(edges) + "]"
        # The HTML document is based on the templates provided http://visjs.org/examples/network
        ret = """<html class="eotss_enabled eotss_slow"><head>
  <title>Network | Basic usage</title>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.19.1/vis.js"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.19.1/vis.css" rel="stylesheet" type="text/css">
  <style type="text/css">
    #mynetwork {
      width: 600px;
      height: 400px;
      border: 1px solid lightgray;
    }
  </style>
</head>
<body>
<p>
  Create a simple network with some nodes and edges.
</p>
<div id="mynetwork"><div class="vis-network" tabindex="900" style="position: relative; overflow: hidden; touch-action: pan-y; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); width: 100%; height: 100%;"><canvas style="position: relative; touch-action: none; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); width: 100%; height: 100%;" width="600" height="400"></canvas></div></div>
<script type="text/javascript">
  // create an array with nodes
  var nodes = new vis.DataSet(""" + nodes + """);
  // create an array with edges
  var edges = new vis.DataSet(""" + edges + """);
  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {};
  var network = new vis.Network(container, data, options);
</script>
</body></html>"""
        return ret

    def opGraph(self, opFile):
        # Wraps the visGraph method with a path for writing output.
        o = open(opFile, "w")
        o.write(self.visGraph())
        o.close()

    def getNode(self, n):
        return self.nodes[n]

    def addNode(self):
        self.nodes.append(node())
        self.active.append(True)

    def connect(self, n1, n2):
        self.nodes[n1].connect(n2)

    def disconnect(self, n1, n2):
        self.nodes[n1].disconnect(n2)

    def remove(self,n):
        try:
            del self.nodes[n]
            del self.active[n]
        except KeyError:
            sys.exc_clear()
        for k in self.nodes:
            k.disconnect(n)

    def activate(self,n):
        self.active[n] = True

    def deactivate(self,n):
        self.active[n] = False

    def flow(self, s):
        # This represents the multilation of the state vector s by the transition matrix for the graph.
        r = self.blankState()
        for n, k in enumerate(self.nodes):
            if self.active[n]:
                for k2 in k.connections:
                    r[k2] += s[n] * k.connections[k2]
        return (r)

    def printOut(self):
        # Prints the transition matrix
        r = ""
        for k in self.nodes:
            keys = k.connections.keys()
            for n, k2 in enumerate(self.nodes):
                r += str(k.connections[n]) if n in keys else "0"
                r += "\t"
            r += "\n"
        return(r)

    def getConnected(self, n1, n2):
        # Test if you can get to n2 from n1 walking along edges in the graph.
        # Returns 0 if a path exists else -1
        g = copy.deepcopy(self)
        # Makes all nodes self connected for the sake of the algo... g is a copy of self becasue
        # calculating a property of the graph should not change the values of the graph, so if we need to make changes
        # for calculation better do it on a copy.
        for n, k in enumerate(g.nodes):
            k.connect(n)
        state = self.blankState()
        state[n1] = 1
        c = 0
        if (state[n2] != 0):
            return (c)
        while c < len(state):
            state = g.flow(state)
            c += 1
            if (state[n2] != 0):
                return (c)
        return -1

    def nFlow(self, state, n):
        # Multiply an state vector by the graphs transition matrix n times, printing at each step.
        c = 0
        print("Graph:"+self.printOut())
        print("Initial-State:"+str(state))
        while (c < n):
            state = self.flow(state)
            print("State-" + str(c + 1) + ":")
            print(state)
            c += 1

    def blankState(self):
        # Generate an empty state vector of appropriate size for the graph.
        return [0] * len(self.nodes)

    def subnets(self):
        #Builds a list of list of node groups.
        r = []
        g = copy.deepcopy(self)
        for n, k in enumerate(g.nodes):
            k.connect(n)
        n = 0
        used = []
        while (n < len(self.nodes)):
            if n in used:
                n += 1
            else:
                state = self.blankState()
                state[n] = 1
                temp = []
                for k in range(0, len(self.nodes)):
                    state = g.flow(state)
                for c, k in enumerate(state):
                    if k != 0:
                        temp.append(c)
                        used.append(c)
                r.append(temp)
                n += 1
        return (r) # Could 1 node end up in 2 different groups? Yes... That is meh...

"""
Test function added 7 nodes to a graph and connects 4 of them in one group and 3 in the other.
I can imagine failing test cases for this whole thing so let's not expect this all to be perfect.
"""


def test():
    g = graph()
    for k in range(0, 7):
        g.addNode()
    for k in range(0, 3):
        g.connect(k, k + 1)
    for k in range(4, 6):
        g.connect(k, k + 1)
    print("pass" if g.getConnected(0, 2) == 2 else "fail")
    s = g.blankState()
    s[0] = 1
    g.nFlow(s, 7)
    print("groupsReshaped:")
    print(g.subnets())
    g.opGraph("graphTest.html")


test()