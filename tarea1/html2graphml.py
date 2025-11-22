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
    html = File().load('./tarea1/prueba.html')

    dom = captureElementsFromHtml(html)

    grafo = ''
    #tipoDeGrafico = menuSalida()
    tipoDeGrafico = 1
    match tipoDeGrafico:
        case 1: # dot
            grafo = GeneradorGrafoDot()
            print(f'Grafo:\n{grafo.generate(dom)}')
            pass
        case 2: # graphml
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