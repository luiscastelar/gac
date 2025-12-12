# Importaciones
from myHTMLParser import MyHTMLParser
                            # parserHTML personalizable
from contentOfFile import File
from elemento import Elemento
#from generadorGrafo import GeneradorGrafo
from generadorGrafoDot import GeneradorGrafoDot

# Constantes
TAB = 4                     # para la impresión del DOM
ANCHO = 120                 # Ancho de pantalla

# Variables globales
numNodo = 0
numArista = 0

TAREA_PATH = './gac/tarea1/'
TEMPLATES_PATH = TAREA_PATH + 'templates/'
TEMPLATE_MAIN = ''
TEMPLATE_KEYS = ''
TEMPLATE_NODES = ''
TEMPLATES_DATAS = ''
TEMPLATE_EDGES = ''


# Main()
def main():
    global TEMPLATE_MAIN, TEMPLATE_KEYS, TEMPLATE_NODES, TEMPLATE_DATAS, TEMPLATE_EDGES

    # Cargamos archivo
    html = File().load(TAREA_PATH + 'prueba.html')

    # string to dom (elemento)
    dom = captureElementsFromHtml(html)
    printElemento(dom,0)       # Imprimimos DOM
    print('---\n')

    # ---------------------------------------------------------------------
    # Comenzamos la generación automática de código partiendo de plantillas
    # ---------------------------------------------------------------------
    grafo = ''
    #tipoDeGrafico = menuSalida()
    tipoDeGrafico = 2
    match tipoDeGrafico:
        case 1: # dot
            grafo = GeneradorGrafoDot()
            print(f'Grafo:\n{grafo.generate(dom)}')
            pass
        case 2: # graphml
            TEMPLATE_MAIN = 'graphml.xml'
            TEMPLATE_KEYS = 'key.graphml'
            TEMPLATE_NODES = 'node.graphml'
            TEMPLATE_DATAS = 'data.graphml'
            TEMPLATE_EDGES = 'edge.graphml'
            claves = getTipoDeAtributos(dom)
            clavesNominadas = {}
            numeral = 0
            for clave in claves:
                clavesNominadas[clave] = f'd{numeral}'
                numeral += 1
            #print(f'Claves: {clavesNominadas}')
            claves = ''
            tipo = 'string'
            for nombre, id in clavesNominadas.items():
                claves += File().load(TEMPLATES_PATH+TEMPLATE_KEYS).replace("<%id%>", id).replace("<%nombre%>", nombre).replace("<%tipo%>", tipo) + '\n'
            print(f'Claves:\n{claves}')

            listaDeNodos, listaDeAristas = getNodosYAristas(dom, clavesNominadas)
            nodos = '\n'.join(listaDeNodos)
            print(f'Nodos:\n{nodos}')
            aristas = '\n'.join(listaDeAristas)
            print(f'Aristas:\n{aristas}')
            
            salida = File().load(TEMPLATES_PATH + TEMPLATE_MAIN)
            salida = salida.replace("<%claves%>", claves)
            salida = salida.replace("<%nodos%>", nodos)
            salida = salida.replace("<%aristas%>", aristas)
            print('---\n')
            print( salida )
            File().save('./gac/salida.graphml', salida)
        case _: # cancelar (por defecto)
            print('¡Hasta otro día!')
    
    quit(1)

    ''' Obsoleto
    printElemento(dom,0)       # Imprimimos DOM

    grafo = dom.str()
    bytesWritted = File().save('./tarea1/prueba.dot',grafo)
    print(f'Se han escrito {bytesWritted} bytes.')

    separador('-')

    #generarGraphml(dom)
    quit(1);
    
    separador('=')
    salida = encabezado()
    salida += addNodoG(root)
    salida += cierre()
    print(f'Salida:\n{salida}')
    robust_write(salida, './salida.dot')


    separador('=')
    G = GeneradorGrafoDot()
    salida = G.generate(root)
    print( salida )
    '''

def getTipoDeAtributos(ele: list[tuple[str, str|None]]):
    atributos = set()
    atributos.add('txt')
    atributos.add('nombre')
    # Mostramos según tengamos atributos o no
    try:
        if len(ele.atributos) > 0 :            
            for att in ele.atributos:
                atributos.add(att[0])
    except:
        pass

    # recorremos los hijos
    for hijo in ele.hijos:
        atributos = atributos | getTipoDeAtributos(hijo) 

    return atributos


def getNodosYAristas(ele: list[tuple[str, str|None]], clavesNominadas: list):
    global numNodo
    global numArista
    nodos = []
    aristas = []
    datos = ''
    
    # Mostramos según tengamos atributos o no
    try:
        #datos += separador(' ')*3 + f'<data key="{ clavesNominadas["nombre"] }">{ele.nombre}</data>' + '\n'
        plantilla = File().load(TEMPLATES_PATH+TEMPLATE_DATAS)
        temp = plantilla.replace("<%key_id%>", clavesNominadas["nombre"])
        temp = temp.replace("<%value%>", ele.nombre)
        datos += temp + '\n'

        if len(ele.atributos) > 0 :            
            for att in ele.atributos:
                #datos += separador(' ')*3 + f'<data key="{clavesNominadas[ att[0] ]}">{att[1]}</data>' + '\n'        
                temp = plantilla.replace("<%key_id%>", clavesNominadas[ att[0] ])
                temp = temp.replace("<%value%>", att[1])
                datos += temp + '\n'
                # Aquí deberíamos pensar si queremos sacar los atributos de "style" como keys o dejarlos como un bloque.
                # Pensemos que, con carácter general, los estilos irán en una hoja CSS externa por separación de responsabilidades.
        else:
            if len(ele.txt) > 0:
                #datos += separador(' ')*3 + f'<data key="{ clavesNominadas["txt"] }">{ele.txt}</data>'+'\n'
                temp = plantilla.replace("<%key_id%>", clavesNominadas[ "txt" ])
                temp = temp.replace("<%value%>", ele.txt)
                datos += temp + '\n'
    except:
        pass

    # Creamos el nodo
    plantilla = File().load(TEMPLATES_PATH+TEMPLATE_NODES)
    temp = plantilla.replace("<%id%>", f'n{numNodo}')
    temp = temp.replace("<%datos%>", datos)
    temp += temp + '\n'
    nodos.append( temp )
    #nodo = separador(' ')*2 + f'<node id="n{numNodo}">' + '\n'
    #nodo += datos
    #nodo += separador(' ')*2 + '</node>'
    #nodos.append( nodo )
    
    # Actualizamos índice
    numNodoPadre = numNodo
    numNodo += 1
    
    # recorremos los hijos
    for hijo in ele.hijos:
        aristas.append( separador(' ')*2 + f'<edge id="e{numArista}" source="n{numNodoPadre}" target="n{numNodo}"/>')
        numArista += 1
        nodHijo, ariHijo =  getNodosYAristas(hijo, clavesNominadas)
        nodos.extend( nodHijo )
        aristas.extend( ariHijo )

    return nodos, aristas


def printElemento(ele,profundidad):
    # Para visualizar el DOM analizado
    # Mostramos según tengamos atributos o no
    try:
        if len(ele.atributos) > 0 :
            print(' '*profundidad + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}')
        else:
            print(' '*profundidad + f'{ele.nombre}: {ele.txt}')
    except:
        pass

    # recorremos los hijos
    for hijo in ele.hijos:
        printElemento(hijo, profundidad+TAB)

def list2str(lista: list[tuple[str, str|None]]):
    # función auxiliar para recorrer los atributos
    str = ""
    for ele in lista:
        str += ele[0] + "->" + ele[1]
    return str

def separador(char: str) -> str:
    return char * TAB

def menuSalida():
    # Menú de selección de salida
    print(f'''
          Menú:
          -----          
          1 - Salida tipo dot
          2 - Salida tipo graphml
          0 - Cancelar
          ''')
    return int( input('Introduce elección: '))

def captureElementsFromHtml(html):
    # Utilizamos un parse para capturar elementos
    parser = MyHTMLParser()
    parser.feed( html )         # cargamos html en nuestro parserHtml
    dom = parser.getRoot();
    parser.close()              # cerramos parser
    return dom


# Cargador externo
if __name__ == "__main__":
     main()