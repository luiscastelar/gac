from generadorGrafo import GeneradorGrafo

# Personalización a Grafo Dot
class GeneradorGrafoDot(GeneradorGrafo):
    
    #grafo = ''

    def __init__(self):
        super().__init__()
        grafo = self.getHead()

    def getHead(self):
        return '''digraph G {
    charset="UTF-8"
'''
    def getFooter(self):
        return '}'


    def generateNodes(self):
        for node in self.getNodes():
            #txt = super().getNodes()
            txt = f'{node.nombre}_{node.uid} [\n'
            txt += self.getKeysFromNode(node)
            txt += '\n]'
            return txt


    def getKeysFromNode(self,node):
        str = ""
        for node in node.atributos:
            str += f'\t{node[0]} = {node[1]} \n'
        return str


    def addEdge(self, A, B):
        self.edges.append(f'{A}->{B}\n')
