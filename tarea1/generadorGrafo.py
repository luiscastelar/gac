class GeneradorGrafo():
    keys = []
    nodes = []
    edges = []

    def generate(self, node):
        self.addNode(node)
        txt = self.getHead()
        txt += self.getKeys()
        txt += self.getNodes()
        txt += self.getEdges()
        txt += self.getFooter()
        return txt

    def getHead(self):
        return ''

    def getFooter(self):
        return ''

    def addKey(key):
        pass

    def addNode(self, node):
        pass

    def addEdge(A, B):
        pass

    def getKeys(self):
        return ''
    
    def getNodes(self):
        return ''
    
    def getEdges(self):
        return ''