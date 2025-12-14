# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------
import logging
import os
from myHTMLParser import MyHTMLParser
                            # parserHTML personalizable
from contentOfFile import File
from elemento import Elemento
from drawGraphml import Graphml

# ---------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------
TAB = 4                     # parametrizamos el ancho de tabulaciones
ANCHO = 120                 # y de la pantalla
LOGGIN = logging.INFO       # modo de depuración
TAREA_PATH = os.path.dirname(__file__) + '/'
                            # capturamos la ruta actual para ser base de 
                            # templates y test
TEMPLATES_PATH = TAREA_PATH + 'templates/'
FILE_LOGGIN = TAREA_PATH + 'app.log'

# ---------------------------------------------------------------------
# # Opciones de depuración:
#  - DEBUG, INFO, WARNING, ERROR, CRITICAL
# ---------------------------------------------------------------------
if LOGGIN == logging.INFO:
    logging.basicConfig(level = LOGGIN,
                        format='%(message)s')
else:
    logging.basicConfig(filename = FILE_LOGGIN,
                        filemode = 'a',
                        level = LOGGIN,
                        format='''%(asctime)s - f:%(module)s:%(lineno)d [%(levelname)s]:\n%(message)s''')

# ---------------------------------------------------------------------
# Variables globales
# ---------------------------------------------------------------------
numNodo = 0
numArista = 0

# "Constantes" de tipo
TEMPLATE_MAIN = ''
TEMPLATE_KEYS = ''
TEMPLATE_NODES = ''
TEMPLATES_DATAS = ''
TEMPLATE_EDGES = ''


# ---------------------------------------------------------------------
# Main()
# ---------------------------------------------------------------------
def main():
    global TEMPLATE_MAIN, TEMPLATE_KEYS, TEMPLATE_NODES, TEMPLATE_DATAS, TEMPLATE_EDGES, tagsParametrizados

    # Cargamos archivo
    #html = File().load(TAREA_PATH + 'test/test1.html')
    html = File().load('')
    logging.info( 'Archivo con Html leído correctamente' )

    # string Html to dom (elementos Html)
    dom = captureElementsFromHtml(html)
    logging.info( 'Str Html parseado correctamente')
    logging.debug( html2str(dom, 0) )
                                # 0 para NO dejar margen en el elemento raíz

    # ---------------------------------------------------------------------
    # Comenzamos la generación automática de código partiendo de plantillas
    # ---------------------------------------------------------------------
    tipoDeGrafico = menuSalida()
    match tipoDeGrafico:
        case 1: # dot
            # 'Constantes' para generar gráficos .DOT
            GRAPH_TYPE = 'dot'
            TEMPLATE_MAIN = 'main.'+GRAPH_TYPE
            TEMPLATE_KEYS = 'key.'+GRAPH_TYPE
            TEMPLATE_NODES = 'node.'+GRAPH_TYPE
            TEMPLATE_DATAS = 'data.'+GRAPH_TYPE
            TEMPLATE_EDGES = 'edge.'+GRAPH_TYPE

            claves = ''         # este formato NO tiene listado de claves
            
            # Obtenemos nodos y aristas como lista y los transformamos en 
            # cadenas de texto para la salida
            listaDeNodos, listaDeAristas = getNodosYAristasDot(dom)
            nodos = ''.join(listaDeNodos)
            logging.debug(f'Nodos:\n{nodos}')
            aristas = '\n'.join(listaDeAristas)
            logging.debug(f'Aristas:\n{aristas}')

        case 2: # graphml
            # 'Constantes' para generar gráficos .graphml
            GRAPH_TYPE = 'graphml'
            TEMPLATE_MAIN = 'main.'+GRAPH_TYPE
            TEMPLATE_KEYS = 'key.'+GRAPH_TYPE
            TEMPLATE_NODES = 'node.'+GRAPH_TYPE
            TEMPLATE_DATAS = 'data.'+GRAPH_TYPE
            TEMPLATE_EDGES = 'edge.'+GRAPH_TYPE

            # Capturamos los distintos tipos de atributos generamos una relación
            # atributo - id único
            clavesNominadas = nominarClaves( getTipoDeAtributos(dom) )

            # Generamos listado de keys
            claves = listadoDeClavesConFormato(clavesNominadas)
            logging.debug(f'Claves:\n{claves}')
            
            # Obtenemos nodos y aristas como lista y los transformamos en 
            # cadenas de texto para la salida
            listaDeNodos, listaDeAristas = getNodosYAristas(dom, clavesNominadas)
            nodos = ''.join(listaDeNodos)
            logging.debug(f'Nodos:\n{nodos}')
            aristas = '\n'.join(listaDeAristas)
            logging.debug(f'Aristas:\n{aristas}')

        case _: # cancelar (por defecto)
            print('¡Hasta otro día!')
            quit(0)



    # Generamos la salida sustituyendo las cadenas generadas de claves, nodos y
    # aristas en la plantilla principal
    salida = File().load(TEMPLATES_PATH + TEMPLATE_MAIN)
    salida = salida.replace("<%claves%>", claves)
    salida = salida.replace("<%nodos%>", nodos)
    salida = salida.replace("<%aristas%>", aristas)
    logging.debug( salida )

    # Exportamos el archivo de salida
    File().save(TAREA_PATH + 'grafos/' + 'salida.'+GRAPH_TYPE, salida)

    logging.info('Hemos finalizado el procesado. Su archivo fue correctamente generado.')

    # Para invocar al renderizador
    if tipoDeGrafico == 2:
        visualizar = input('¿Desea visualizar el resultado? [s/N]: ')
        if visualizar.lower() == 's' and tipoDeGrafico == 2:
            try:
                Graphml.draw(TAREA_PATH + 'grafos/' + 'salida.'+GRAPH_TYPE)
            except:
                logging.info('''La generación del grafo ha fallado.
                             Probablemente NO tengas instalado en el sistema la librería NetworkX.
                             Para proceder a instalarla abre una terminal (bash/cmd/powershell) y escribe:
                             pip install networkx
                             En caso de fallo o incompatibilidad con tu S.O. puedes cargar un entorno virtual y realizar la instalación anterior.
                             Para ello sigue lo indicado en https://medium.com/@diego.coder/generaci%C3%B3n-de-entornos-virtuales-con-venv-en-python-3-bd374a173129''')
    quit(0)


# ---------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------
def listadoDeClavesConFormato(clavesNominadas):
    # Realiza la sustitución de los pares de claves-id en la plantilla generando
    # el string de claves
    claves = ''
    tipo = 'string'
    for nombre, id in clavesNominadas.items():
        # Procesamos la plantilla sustituyendo las keys por sus valores
        claves += File().load(TEMPLATES_PATH+TEMPLATE_KEYS).replace("<%id%>", id).replace("<%nombre%>", nombre).replace("<%tipo%>", tipo) + '\n'
    return claves


def nominarClaves(claves):
    # generamos id único a cada clave y devolvemos una lista con la relación
    # nombres - ids
    clavesNominadas = {}
    numeral = 0
    for clave in claves:
        clavesNominadas[clave] = f'd{numeral}'
        numeral += 1

    return clavesNominadas


def getTipoDeAtributos(ele: list[tuple[str, str|None]]):
    # Función RECURSIVA que recorre el dom tomando los atributos para las 
    # keys de algunos generadores de grafos (como Graphml) 
    
    # Creamos el set de atributos con los que SIEMPRE van a aparecer
    atributos = set()
    atributos.add('label')
    atributos.add('txt')
    atributos.add('name')
    
    try:
        if len(ele.atributos) > 0 :
            # Capturamos los nombres de atributos para las claves
            for att in ele.atributos:
                atributos.add(att[0])
    except:
        pass

    # recorremos los hijos de forma análoga añadiendo los resultados al set
    for hijo in ele.hijos:
        atributos = atributos | getTipoDeAtributos(hijo) 

    # Retornamos el set
    return atributos


def getNodosYAristasDot(ele: list[tuple[str, str|None]]):
    # Función RECURSIVA que recorre el dom tomando NODOs y ARISTAS

    # Necesitamos continuar la cuenta para no repetir identificadores
    global numNodo
    global numArista
    nodos = []
    aristas = []
    datos = ''
    
    # Generamos el string con los datos (valor de los atributos) de los nodos
    try:
        # Compenzamos cargando la plantilla y sustituyendo la etiqueta con el 
        # nombre del tag
        plantilla = File().load(TEMPLATES_PATH+TEMPLATE_DATAS)
        temp = plantilla.replace("<%key_id%>", 'label')  # o con key 'label'
        temp = temp.replace("<%value%>", ele.nombre)
        datos += temp + '\n'

        if len(ele.atributos) > 0 :            
            for att in ele.atributos:
                # Añadimos cada atributo con su clave
                temp = plantilla.replace("<%key_id%>", att[0] )
                temp = temp.replace("<%value%>", att[1])
                datos += temp + '\n'
                # Aquí deberíamos pensar si queremos sacar los atributos de 
                # "style" como keys o dejarlos como un bloque.
                # Pensemos que, con carácter general, los estilos irán en una 
                # hoja CSS externa por separación de responsabilidades por lo 
                # que aporta poco realizar este procesado
        else:
            if len(ele.txt) > 0:
                # Añadimos el contenido de texto plano
                temp = plantilla.replace("<%key_id%>", "txt" )
                temp = temp.replace("<%value%>", ele.txt)
                datos += temp + '\n'
    except:
        pass

    # Creamos el nodo sustituyendo en la plantilla con el id único de nodo 
    # y los datos obtenidos en el paso anterior
    plantilla = File().load(TEMPLATES_PATH+TEMPLATE_NODES)
    temp = plantilla.replace("<%id%>", f'n{numNodo}')
    temp = temp.replace("<%datos%>", datos[:-1])  # debemos eliminar el último
                                                  # carácter para no tener saltos
                                                  # de página extra
    temp += '\n'
    nodos.append( temp )
    
    # Actualizamos índice
    numNodoPadre = numNodo
    numNodo += 1
    
    # Cargamos la plantilla de generación de aristas
    plantillaArista = File().load(TEMPLATES_PATH+TEMPLATE_EDGES)
    
    for hijo in ele.hijos:
        # recorremos los hijos sustituyendo los ids de origen y destino en las
        # aristas
        temp = plantillaArista.replace("<%origen_id%>", f'n{numNodoPadre}')
        temp = temp.replace("<%destino_id%>", f'n{numNodo}')
        temp += '\n'
        aristas.append( temp )  # añadimos a la lista de aristas
        numArista += 1
        # llamamos recursivamente a la función con los hijos
        nodHijo, ariHijo =  getNodosYAristasDot(hijo)

        # añadimos nodos y aristas del hijo en la lista de nodos y aristas
        nodos.extend( nodHijo )
        aristas.extend( ariHijo )

    return nodos, aristas


def getNodosYAristas(ele: list[tuple[str, str|None]], clavesNominadas: list):
    # Función RECURSIVA que recorre el dom tomando NODOs y ARISTAS y asociándolos
    # con los identificadores de las keys obtenidas en el paso "getTipoDeAtributos"
    #
    # Esto es, al contrario que la específica del .DOT, en esta tenemos que asociar
    # los datos del nodo con las claves a través de sus identificadores por lo 
    # que requerimos algún paso adicional, pero la mecánica de sustitución es 
    # similar.

    # Necesitamos continuar la cuenta para no repetir identificadores
    global numNodo
    global numArista
    nodos = []
    aristas = []
    datos = ''
    
    # Mostramos según tengamos atributos o no
    try:
        # En este caso debemos tomar el id de la clave 'name' y no el nombre directamente
        plantilla = File().load(TEMPLATES_PATH+TEMPLATE_DATAS)
        temp = plantilla.replace("<%key_id%>", clavesNominadas["name"])  # o con key 'label'
        temp = temp.replace("<%value%>", ele.nombre)
        datos += temp + '\n'

        if len(ele.atributos) > 0 :            
            for att in ele.atributos:
                # En este caso debemos tomar el id de la clave y no el nombre de atributo directamente
                temp = plantilla.replace("<%key_id%>", clavesNominadas[ att[0] ])
                temp = temp.replace("<%value%>", att[1])
                datos += temp + '\n'
        else:
            if len(ele.txt) > 0:
                # En este caso debemos tomar el id de la clave 'txt' y no el nombre directamente
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
    
    # Cargamos la plantilla de generación de aristas
    plantillaArista = File().load(TEMPLATES_PATH+TEMPLATE_EDGES)
    
    # recorremos los hijos
    for hijo in ele.hijos:
        temp = plantillaArista.replace("<%edge_id%>", f'{numArista}')
        temp = temp.replace("<%origen_id%>", f'{numNodoPadre}')
        temp = temp.replace("<%destino_id%>", f'{numNodo}')
        aristas.append( temp )  # añadimos a la lista de aristas
        numArista += 1

        nodHijo, ariHijo =  getNodosYAristas(hijo, clavesNominadas)
        nodos.extend( nodHijo )
        aristas.extend( ariHijo )

    return nodos, aristas


def html2str(ele: Elemento, margen: int) -> str:
    # Función RECURSIVA que recorre el Elemento y sus hijos como objetos y 
    # retorna un str (para depuración)
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
    # De str Html a objeto 'Html'
    try:
        # Utilizamos un analizador externo para capturar elementos
        parser = MyHTMLParser()
        parser.feed( html )         # cargamos html en nuestro parserHtml
        dom = parser.getRoot();
        parser.close()              # cerramos parser
        return dom
    except:
        print('Fallo de parseo de html')
        quit(1)



# Autocargador de programa externo
if __name__ == "__main__":
     main()