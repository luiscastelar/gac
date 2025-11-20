from generadorGrafo import GeneradorGrafo

# Personalización a Grafo Dot
class GeneradorGrafoDot(GeneradorGrafo):
    def getHead(self):
        return '''digraph G {
    charset="UTF-8"
'''
    def getFooter(self):
        return '}'

    def addNode(self, node):
        idNode = f'{node.nombre}_{node.uid}'
        self.nodes.append(f'{idNode} [{getAtributos(node.atributos)}]\n')

    def addEdge(self, A, B):
        self.edges.append(f'{A}->{B}\n')
