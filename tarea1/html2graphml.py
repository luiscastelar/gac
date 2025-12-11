# Importaciones
#from html.parser import HTMLParser
from myHTMLParser import MyHTMLParser
                            # parserHTML personalizable
from contentOfFile import File
from elemento import Elemento
#from generadorGrafo import GeneradorGrafo
from generadorGrafoDot import GeneradorGrafoDot

#import re                   # Expresionse regulares
#import networkx as nx       # generador de grafos
#import graphviz             # para dibujar el grafo
#import os

# Constantes
TAB = 4                     # para la impresión del DOM
ANCHO = 120                 # Ancho de pantalla

# Variables globales
#root = None
#actual = None



# Main()
def main():
    # Cargamos archivo
    html = File().load('./gac/tarea1/prueba.html')

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
            TEMPLATE = './templates/graphml.xml'
            claves = getTipoDeAtributos(dom)
            print(claves)
            #nodos, aristas = getNodosYAristas(dom)
            #salida = reemplazar(TEMPLATE, 'claves', claves)
            #salida = reemplazar(salida, 'nodos', nodos)
            #salida = reemplazar(salida, 'aristas', aristas)
            
            pass
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

# Para visualizar el DOM analizado
def printElemento(ele,profundidad):
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

# función auxiliar para recorrer los atributos
def list2str(lista: list[tuple[str, str|None]]):
    str = ""
    for ele in lista:
        str += ele[0] + "->" + ele[1]
    return str

def separador(char):
    print(char * ANCHO)


def menuSalida():
    print(f'''
          Menú:
          -----          
          1 - Salida tipo dot
          2 - Salida tipo graphml
          0 - Cancelar
          ''')
    return int( input('Introduce elección: '))






# Utilizamos un parse para capturar elementos
def captureElementsFromHtml(html):
    parser = MyHTMLParser()
    parser.feed( html )         # cargamos html en nuestro parserHtml
    dom = parser.getRoot();
    parser.close()              # cerramos parser
    return dom


# Cargador externo
if __name__ == "__main__":
     main()