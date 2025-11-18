# Importaciones
from html.parser import HTMLParser
                            # parserHTML personalizable
import re                   # Expresionse regulares
#import networkx as nx       # generador de grafos
#import graphviz             # para dibujar el grafo
import os

# Constantes
TAB = 4                     # para la impresión del DOM
ANCHO = 120                 # Ancho de pantalla

# Variables globales
root = None
actual = None
uid = 0;
tipoDeGrafico = 'dot'

# Generador de Unique Id
def getUId():
    global uid
    esteId = uid
    uid = esteId + 1
    return esteId


# Clase Elemento HTML
class Elemento:
    def __init__(self, nombre):
        self.uid = getUId() # para evitar colisiones en los grafos
        self.nombre = nombre
        self.txt = ''       # texto plano
        self.atributos = []
        self.hijos = []     # Elementos hijos anidados
        self.padre = None   # Elemento padre del que cuelga

    # Asigno padre (para vincularlo y poderlo recorrer)
    def asignarPadre(self, ele):
        self.padre = ele

    # Añado un elemento anidado
    def addHijo(self, ele):
        self.hijos.append(ele)

    # Asigno valor 
    def setTxt(self, txt):
        self.txt = txt

# Extensión de un parser sencillo
class MyHTMLParser(HTMLParser):

    # Cuando encuentra un tag de apertura
    def handle_starttag(self, tag, attrs):
        global root
        global actual

        # Creamos elemento
        ele = Elemento(tag)
        if root == None:
            # Si no existía ningún elemento lo tomamos como raíz y actual (para asignar hijos)
            root = ele
            actual = ele
        else:
            ele.asignarPadre(actual)    # Le asignamos el padre para recorrer hacia afuera
            actual.hijos.append(ele)    # Al actual le asignamos el elemento por estar anidado. Es un hijo 
            actual = ele                # Recorreremos el elemento en busca de hijos

        #print("Encountered a start tag:", tag)
        if len(attrs) > 0:
            #print("Atributos: " + list2str(attrs))
            ele.atributos = attrs        # guardamos la lista de atributos

    # Cuando encuentra el cierre de etiqueta
    def handle_endtag(self, tag):
        global actual
        if actual != root:
            # subimos al nivel superior
            actual = actual.padre
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        global actual
        # Si hay texto
        if len(data.strip()) > 0:
            #print("Encountered some data  :", data)
            texto = re.sub(r'\n|\s{2,}', r' ', data)  # eliminamos saltos de página '\n' y espacios dobles
            actual.setTxt(texto)        # asignamos texto


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

    


# función auxiliar para recorrer los atributos
def list2str(lista: list[tuple[str, str|None]]):
        str = ""
        for ele in lista:
            str += ele[0] + "->" + ele[1]
        return str


# Para visualizar el DOM analizado
def printElemento(ele,profundidad):
    # Mostramos según tengamos atributos o no
    if len(ele.atributos) > 0 :
        print(' '*profundidad + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}')
    else:
        print(' '*profundidad + f'{ele.nombre}: {ele.txt}')

    # recorremos los hijos
    for hijo in ele.hijos:
        printElemento(hijo, profundidad+TAB)


# Para visualizar el DOM analizado
def addNodo(grafo, nodo):
    idNodo = f'{nodo.nombre}_{nodo.uid}'
    # Por defecto queremos rojo las cajas de texto y azul lo demás
    colorNodo = 'red' if idNodo in ['div', 'p', 'span', 'h1'] else 'blue'
    
    # Creamos nodo
    grafo.add_node(idNodo, color=colorNodo)

    # Personalizamos según los atributos o no
    if len(nodo.atributos) > 0 :
        for att in nodo.atributos:
            match att[0]:
                case 'id':  # Añadimos id
                    grafo.add_node(idNodo, id=att[1])
                case 'style': 
                    estilos = att[1].split(';')
                    for estilo in estilos:
                        if estilo.startswith('color'):  # Cambiamos color
                            colorDeForma = estilo.split(':')[1].strip()
                            grafo.add_node(idNodo, color=colorDeForma)
                case 'src':  # Muestra la imagen
                    grafo.add_node(idNodo, image=att[1])
                case _:
                    print(f'Atributo desconocido: {att[0]}->{att[1]}')
                    pass
        #print(' '*profundidad + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}')
        pass
    else:
        #print(' '*profundidad + f'{ele.nombre}: {ele.txt}')
        pass
    
    # Si tiene texto lo añadimos como label. Podríamos añadir un nodo hijo con forma plaintext
    if len(nodo.txt) > 0:
        idNodoTexto = f'{nodo.txt}_{getUId()}'
        grafo.add_node(idNodoTexto, shape='plaintext')
        grafo.add_edge(idNodo, idNodoTexto)

    # recorremos los hijos de forma recursiva
    for hijo in nodo.hijos:
        addNodo(grafo, hijo)
        idNodoHijo = f'{hijo.nombre}_{hijo.uid}'
        grafo.add_edge(idNodo, idNodoHijo)
    

def generarGraphml(DOM):
    #G = nx.Graph()                      # crear un grafo
    #G.__setattr__("charset", "UTF-8")
    #addNodo(G, DOM)                     # creamos recursivamente nodos a partir del nodo raíz
    #nx.write_graphml(G, "prueba.graphml")
                                        # escribimos archivo de salida
    #nx.write_latex(G, "prueba.latex")                                

    #A = nx.nx_agraph.to_agraph(G)
    #A.layout('dot')
    #A.draw('salida.png') # guardar como png
    pass
    

def addNodoG(nodo):
    grafo = ''
    idNodo = f'{nodo.nombre}_{nodo.uid}'
    
    # Por defecto queremos rojo las cajas de texto y azul lo demás
    colorNodo = 'red' if idNodo in ['div', 'p', 'span', 'h1'] else 'blue'
    nodo.atributos.append(('color', colorNodo))

    for att in nodo.atributos:
        print(att)
    #atributos.append(f'color={colorNodo}')
    
    # Personalizamos según los atributos o no
    if len(nodo.atributos) > 0 :
        for att in nodo.atributos:
            match att[0]:
                case 'id':  # Añadimos id
                    #grafo.add_node(idNodo, id=att[1])
                    pass
                case 'style': 
                    estilos = att[1].split(';')
                    for estilo in estilos:
                        if estilo.startswith('color'):  # Cambiamos color
                            colorDeForma = estilo.split(':')[1].strip()
                            #grafo.add_node(idNodo, color=colorDeForma)
                case 'src':  # Muestra la imagen
                    #grafo.add_node(idNodo, image=att[1])
                    pass
                case _:
                    #print(f'Atributo desconocido: {att[0]}->{att[1]}')
                    pass
        #print(' '*profundidad + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}')
        pass
    else:
        #print(' '*profundidad + f'{ele.nombre}: {ele.txt}')
        pass

    # Creamos nodo
    #grafo.add_node(idNodo, color=colorNodo)

    # Si tiene texto lo añadimos como label. Podríamos añadir un nodo hijo con forma plaintext
    nodo.atributos.append(('label', nodo.txt if len(nodo.txt)>0 else nodo.nombre))
    '''
    if len(nodo.txt) > 0:
        nodo.atributos.append(('label', nodo.txt))
    else:
        nodo.atributos.append(('label', nodo.nombre))
    '''

    # Generación Graph.dot
    grafo += f'{idNodo} [{getAtributos(nodo.atributos)}]\n'

    

    # recorremos los hijos de forma recursiva
    for hijo in nodo.hijos:
        grafo += addNodoG(hijo)
        idNodoHijo = f'{hijo.nombre}_{hijo.uid}'
        #grafo.add_edge(idNodo, idNodoHijo)
        grafo += addEdgeG(idNodo, idNodoHijo)

    return grafo

def addEdgeG(nodo, hijo):
    return f'{nodo}->{hijo}\n'

def encabezado():
    match tipoDeGrafico:
        case 'dot':
            return '''digraph G {
  charset="UTF-8"
  '''
        case _:
            raise Exception('Tipo de gráfico NO válido')

def cierre():
    match tipoDeGrafico:
        case 'dot':
            return '}'
        case _:
            raise Exception('Tipo de gráfico NO válido')


def getAtributos(atributos):
    salida = ''
    for att in atributos:
        salida += f'{att[0]}="{att[1]}"\n'
    return salida
    

def robust_write(text, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    except IOError as e:
        print(f'Write failed: {e}')


# Main()
def main():
    global DOM

    # Creamos el parserHTML
    parser = MyHTMLParser()

    # Tomamos un html de ejemplo
    html = '''
    <html>
        <head>
            <title>Test</title>
        </head>
        <body>
            <header>Cabecera</header>
            <main>            
                <h1 id="titulo">Parse me!</h1>
                <div class="ppal">Texto principal
                    <hr />
                    <p>Otro <b style="color: gray;">párrafo</b></p>
                </div>
                <div><img src="fuente.jpg" /></div>
                <div></div>
            </main>
        </body>
    </html>
    '''

    #html = '''<div>hola mundo</div>'''
    parser.feed( html )         # cargamos html en nuestro parserHtml
    parser.close()              # cerramos parser

    printElemento(root,0)       # Imprimimos 
    print('-'*ANCHO)

    generarGraphml(root)
    
    print('='*ANCHO)
    salida = encabezado()
    salida += addNodoG(root)
    salida += cierre()
    print(f'Salida:\n{salida}')
    robust_write(salida, './salida.dot')


    print('='*ANCHO)
    G = GeneradorGrafoDot()
    salida = G.generate(root)
    print( salida )
    


    #global tipoDeGrafico
    #tipoDeGrafico = 'graphml'
    #generarGraph(root)

# Cargador externo
if __name__ == "__main__":
     main()