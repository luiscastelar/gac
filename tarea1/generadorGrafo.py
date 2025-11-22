class GeneradorGrafo():
    keys = []
    nodes = []
    edges = []

    def generate(self, node):
        self.addNode(node)
        txt = self.generateHead()
        txt += self.generateKeys()
        txt += self.generateNodes()
        txt += self.generateEdges()
        txt += self.generateFooter()
        return txt

    def generateHead(self):
        return ''

    def generateFooter(self):
        return ''

    def generateKeys(self):
        return ''
    
    def generateNodes(self):
        return ''
    
    def generateEdges(self):
        return ''

    def addKey(key):
        pass

    def addNode(self, node):        
        # Mostramos según tengamos atributos o no
        if len(node.atributos) > 0 :
            for attr in node.atributos:
                self.keys.append({attr[0], attr[1]})

        self.printElemento(node, 0)
        try:
            self.nodes.append(node)
            # recorremos los hijos
            for hijo in node.hijos:
                self.addNode(hijo)
        except:
            pass
        

    def addEdge(A, B):
        pass

    def getKeys(self):
        return self.keys
    
    def getNodes(self):
        return self.nodes
        
    def getEdges(self):
        return self.edges
    

    
    # función auxiliar para recorrer los atributos
    def list2str(lista: list[tuple[str, str|None]]):
        str = ""
        for ele in lista:
            str += ele[0] + "->" + ele[1]
        return str
    
    # Para visualizar el DOM analizado
    def printElemento(self, ele,profundidad):
        # Mostramos según tengamos atributos o no
        try:
            if len(ele.atributos) > 0 :
                print(' '*profundidad + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}')
            else:
                print(' '*profundidad + f'{ele.nombre}: {ele.txt}')
        except:
            pass

        # recorremos los hijos
        #for hijo in ele.hijos:
        #    printElemento(hijo, profundidad+TAB)
    
