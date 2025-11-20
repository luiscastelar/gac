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
    file = File()
    html = file.load('./tarea1/prueba.html')

    # Utilizamos un parse para capturar elementos
    parser = MyHTMLParser()
    parser.feed( html )         # cargamos html en nuestro parserHtml
    dom = parser.getRoot();
    parser.close()              # cerramos parser

    tipoDeGrafico = menuSalida()
    match tipoDeGrafico:
        case 1: # dot
            pass
        case 2: # graphml
            pass
        case _: # cancelar (por defecto)
            print('¡Hasta otro día!')
    



    printElemento(dom,0)       # Imprimimos DOM

    grafo = dom.str()
    bytesWritted = file.save('./tarea1/prueba.dot',grafo)
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
    


    #global tipoDeGrafico
    #tipoDeGrafico = 'graphml'
    #generarGraph(root)


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


# función auxiliar para recorrer los atributos
def list2str(lista: list[tuple[str, str|None]]):
        str = ""
        for ele in lista:
            str += ele[0] + "->" + ele[1]
        return str


# Cargador externo
if __name__ == "__main__":
     main()