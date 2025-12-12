# Importaciones
import logging
from myHTMLParser import MyHTMLParser
                            # parserHTML personalizable
from contentOfFile import File
from elemento import Elemento
#from generadorGrafo import GeneradorGrafo
from generadorGrafoDot import GeneradorGrafoDot

# Constantes
TAB = 4                     # para la impresión del DOM
ANCHO = 120                 # Ancho de pantalla
LOGGIN = logging.DEBUG
TAREA_PATH = './gac/tarea1/'
TEMPLATES_PATH = TAREA_PATH + 'templates/'
FILE_LOGGIN = TAREA_PATH + 'app.log'

# Opciones de depuración:
#  - DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(filename = FILE_LOGGIN,
                    filemode = 'a',
                    level = LOGGIN,
                    format='''%(asctime)s - f:%(module)s:%(lineno)d [%(levelname)s]:\n%(message)s ''')

# Variables globales
numNodo = 0
numArista = 0

# "Constantes" de tipo
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
    #html = File().load('')

    # string Html to dom (elementos Html)
    dom = captureElementsFromHtml(html)
    logging.debug( html2str(dom, 0) )
                                # 0 para NO dejar margen

    # ---------------------------------------------------------------------
    # Comenzamos la generación automática de código partiendo de plantillas
    # ---------------------------------------------------------------------
    grafo = ''
    #tipoDeGrafico = menuSalida()
    tipoDeGrafico = 1
    match tipoDeGrafico:
        case 1: # dot
            #grafo = GeneradorGrafoDot()
            #print(f'Grafo:\n{grafo.generate(dom)}')
            GRAPH_TYPE = 'dot'
            TEMPLATE_MAIN = 'main.'+GRAPH_TYPE
            TEMPLATE_KEYS = 'key.'+GRAPH_TYPE
            TEMPLATE_NODES = 'node.'+GRAPH_TYPE
            TEMPLATE_DATAS = 'data.'+GRAPH_TYPE
            TEMPLATE_EDGES = 'edge.'+GRAPH_TYPE

            claves = ''
            listaDeNodos, listaDeAristas = getNodosYAristasDot(dom)
            nodos = ''.join(listaDeNodos)
            logging.debug(f'Nodos:\n{nodos}')
            aristas = '\n'.join(listaDeAristas)
            logging.debug(f'Aristas:\n{aristas}')

        case 2: # graphml
            GRAPH_TYPE = 'graphml'
            TEMPLATE_MAIN = 'main.'+GRAPH_TYPE
            TEMPLATE_KEYS = 'key.'+GRAPH_TYPE
            TEMPLATE_NODES = 'node.'+GRAPH_TYPE
            TEMPLATE_DATAS = 'data.'+GRAPH_TYPE
            TEMPLATE_EDGES = 'edge.'+GRAPH_TYPE

            claves = getTipoDeAtributos(dom)
            clavesNominadas = {}
            numeral = 0
            for clave in claves:
                clavesNominadas[clave] = f'd{numeral}'
                numeral += 1
            claves = ''
            tipo = 'string'
            for nombre, id in clavesNominadas.items():
                claves += File().load(TEMPLATES_PATH+TEMPLATE_KEYS).replace("<%id%>", id).replace("<%nombre%>", nombre).replace("<%tipo%>", tipo) + '\n'
            logging.debug(f'Claves:\n{claves}')
            
            listaDeNodos, listaDeAristas = getNodosYAristas(dom, clavesNominadas)
            nodos = ''.join(listaDeNodos)
            logging.debug(f'Nodos:\n{nodos}')
            aristas = '\n'.join(listaDeAristas)
            logging.debug(f'Aristas:\n{aristas}')            
        case _: # cancelar (por defecto)
            print('¡Hasta otro día!')



    # Generamos la salida
    salida = File().load(TEMPLATES_PATH + TEMPLATE_MAIN)
    salida = salida.replace("<%claves%>", claves)
    salida = salida.replace("<%nodos%>", nodos)
    salida = salida.replace("<%aristas%>", aristas)
    logging.debug( salida )
    File().save(TAREA_PATH + 'salida.'+GRAPH_TYPE, salida)

    print('Hemos finalizado el procesado. Su archivo fue correctamente generado.')
    quit(1)


def getTipoDeAtributos(ele: list[tuple[str, str|None]]):
    atributos = set()
    atributos.add('label')
    atributos.add('txt')
    atributos.add('name')
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



def getNodosYAristasDot(ele: list[tuple[str, str|None]]):
    global numNodo
    global numArista
    nodos = []
    aristas = []
    datos = ''
    
    # Mostramos según tengamos atributos o no
    try:
        plantilla = File().load(TEMPLATES_PATH+TEMPLATE_DATAS)
        temp = plantilla.replace("<%key_id%>", 'label')  # o con key 'label'
        temp = temp.replace("<%value%>", ele.nombre)
        datos += temp + '\n'

        if len(ele.atributos) > 0 :            
            for att in ele.atributos:
                temp = plantilla.replace("<%key_id%>", att[0] )
                temp = temp.replace("<%value%>", att[1])
                datos += temp + '\n'
                # Aquí deberíamos pensar si queremos sacar los atributos de "style" como keys o dejarlos como un bloque.
                # Pensemos que, con carácter general, los estilos irán en una hoja CSS externa por separación de responsabilidades.
        else:
            if len(ele.txt) > 0:
                temp = plantilla.replace("<%key_id%>", "txt" )
                temp = temp.replace("<%value%>", ele.txt)
                datos += temp + '\n'
    except:
        pass

    # Creamos el nodo
    plantilla = File().load(TEMPLATES_PATH+TEMPLATE_NODES)
    temp = plantilla.replace("<%id%>", f'n{numNodo}')
    temp = temp.replace("<%datos%>", datos[:-1])
    temp += '\n'
    nodos.append( temp )
    
    # Actualizamos índice
    numNodoPadre = numNodo
    numNodo += 1
    
    plantillaArista = File().load(TEMPLATES_PATH+TEMPLATE_EDGES)
    # recorremos los hijos
    for hijo in ele.hijos:
        #aristas.append( separador(' ')*2 + f'<edge id="e{numArista}" source="n{numNodoPadre}" target="n{numNodo}"/>')
        temp = plantillaArista.replace("<%origen_id%>", f'n{numNodoPadre}')
        temp = temp.replace("<%destino_id%>", f'n{numNodo}')
        temp += '\n'
        aristas.append( temp )
        numArista += 1
        nodHijo, ariHijo =  getNodosYAristasDot(hijo)
        nodos.extend( nodHijo )
        aristas.extend( ariHijo )

    return nodos, aristas

def getNodosYAristas(ele: list[tuple[str, str|None]], clavesNominadas: list):
    global numNodo
    global numArista
    nodos = []
    aristas = []
    datos = ''
    
    # Mostramos según tengamos atributos o no
    try:
        plantilla = File().load(TEMPLATES_PATH+TEMPLATE_DATAS)
        temp = plantilla.replace("<%key_id%>", clavesNominadas["name"])  # o con key 'label'
        temp = temp.replace("<%value%>", ele.nombre)
        datos += temp + '\n'

        if len(ele.atributos) > 0 :            
            for att in ele.atributos:
                temp = plantilla.replace("<%key_id%>", clavesNominadas[ att[0] ])
                temp = temp.replace("<%value%>", att[1])
                datos += temp + '\n'
                # Aquí deberíamos pensar si queremos sacar los atributos de "style" como keys o dejarlos como un bloque.
                # Pensemos que, con carácter general, los estilos irán en una hoja CSS externa por separación de responsabilidades.
        else:
            if len(ele.txt) > 0:
                temp = plantilla.replace("<%key_id%>", clavesNominadas[ "txt" ])
                temp = temp.replace("<%value%>", ele.txt)
                datos += temp + '\n'
    except:
        pass

    # Creamos el nodo
    plantilla = File().load(TEMPLATES_PATH+TEMPLATE_NODES)
    temp = plantilla.replace("<%id%>", f'n{numNodo}')
    temp = temp.replace("<%datos%>", datos[:-1])
    temp += '\n'
    nodos.append( temp )
    
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


def html2str(ele: Elemento, margen: int) -> str:
    # Retorna el Elemento e hijos en forma de str
    # Mostramos según tengamos atributos o no
    salida = ''
    try:
        if len(ele.atributos) > 0 :
            salida += ' '*margen + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}\n'
        else:
            salida += ' '*margen + f'{ele.nombre}: {ele.txt}\n'
    except:
        pass

    # recorremos los hijos
    for hijo in ele.hijos:
        salida += html2str(hijo, margen+TAB)

    return salida


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