import networkx as nx
import matplotlib.pyplot as plt

class Graphml:
    
    def draw(pathToFile):
        # 1. Create a NetworkX graph (or read from GraphML)
        G = nx.read_graphml(pathToFile)

        # 2. Draw the graph
        nx.draw(G, with_labels=True, node_color='lightgreen', edge_color='gray')

        # 3. Add title and show plot
        plt.title("Grafo")
        plt.show()
