# Importaciones
from contentOfFile import File
from elemento import Elemento
from htmlTokenizer import HtmlTokenizer
from htmlScanner import HtmlScanner

#import re                   # Expresionse regulares
#import os

# Constantes
TAB = 4                     # para la impresión del DOM
ANCHO = 120                 # Ancho de pantalla

# Variables globales



# Main()
def main():
    # Cargamos archivo
    html = File().load('./tarea1/prueba.html')

    dom = parseFromHtml(html)

    grafo = ''
    #tipoDeGrafico = menuSalida()
    tipoDeGrafico = 1
    match tipoDeGrafico:
        case 1: # dot
            #grafo = GeneradorGrafoDot()
            #print(f'Grafo:\n{grafo.generate(dom)}')
            pass
        case 2: # graphml
            pass
        case _: # cancelar (por defecto)
            print('¡Hasta otro día!')
    
    quit(1)

    


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
def parseFromHtml(html):
    tokennizer = HtmlTokenizer()
    tokennizer.parse(html)
    for txt in tokennizer.tokens:
        print(txt)

    languagescanner = HtmlScanner()
    htmlElements = languagescanner.parse( tokennizer.tokens )
    for ele in htmlElements:
        print(ele)
    dom = ''
    return dom


# Cargador externo
if __name__ == "__main__":
     main()