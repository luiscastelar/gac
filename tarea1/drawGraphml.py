import networkx as nx
import matplotlib.pyplot as plt


TAREA_PATH = './gac/tarea1/'


# 1. Create a NetworkX graph (or read from GraphML)
#G = nx.Graph()
#G.add_edges_from([(1, 2), (1, 3), (2, 4)])
G = nx.read_graphml(TAREA_PATH + 'salida.graphml')

# 2. Draw the graph
nx.draw(G, with_labels=True, node_color='lightgreen', edge_color='gray')

# 3. Add title and show plot
plt.title("Basic NetworkX Graph")
plt.show()
