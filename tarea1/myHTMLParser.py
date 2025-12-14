from html.parser import HTMLParser
from elemento import Elemento
import re
import csv
import os


class MyHTMLParser(HTMLParser):
    r""" Extensión de un parser sencillo.
    En él capturamos recursivamente los elementos Html y generamos un objeto Elemento.
    
    Importación: HTMLParser, Elemento y el módulo re"""


    TAREA_PATH = os.path.dirname(__file__) + '/'
                            # capturamos la ruta actual para ser base de 
                            # templates y test

    # Variables globales
    root = None
    actual = None
    tagsPersonalizados = []
    tagsParametrizados = []

    def __init__(self, *, convert_charrefs = True):
        super().__init__(convert_charrefs=convert_charrefs)
        # Cargamos tag parametrizados. Los que no aparecen toman valores por defecto
        self.tagsPersonalizados,self.tagsParametrizados = self.importCSV(self.TAREA_PATH + 'parametrizacion/base.csv')
        print(f'Tags personalizados:\n{self.tagsPersonalizados}')

    def handle_starttag(self, tag, attrs):
        r"""Cuando encuentra un tag de apertura creamos el objeto Elemento, asociamos con su padre (o lo declaramos como root del dom) y le cargamos los atributos y una lista de elementos hijo."""

        # Creamos elemento
        ele = Elemento(tag)
        if self.root == None:
            # Si no existía ningún elemento lo tomamos como raíz y actual (para asignar hijos)
            self.root = ele
            self.actual = ele
        else:
            ele.asignarPadre(self.actual)   # Le asignamos el padre para recorrer hacia arriba
            self.actual.hijos.append(ele)   # Al actual (el padre) le asignamos 
                                            # el elemento por estar anidado (es 
                                            # un hijo)
            self.actual = ele               # Actualizamos el puntero

        if len(attrs) > 0:
            # El elemento tiene atributos con lo que los guardamos
            ele.atributos = attrs

        # Parte 2 del ejercicio:
        if ele.nombre in self.tagsPersonalizados:
            print(f'Nombre: {ele.nombre}')
        

    
    def handle_endtag(self, tag):
        r"""Cuando encuentra el cierre de etiqueta continuamos recorriendo los elementos del padre."""

        if self.actual != MyHTMLParser.root:
            # Si el actual no es el root debemos subir al padre del actual
            self.actual = self.actual.padre


    def handle_data(self, data):
        r"Tomamos el contenido (txt) del tag y lo cargadmos en el Elemento."
        if len(data.strip()) > 0:
            texto = re.sub(r'\n|\s{2,}', r' ', data)
                                            # eliminamos saltos de página '\n' 
                                            # y espacios dobles
            self.actual.addTxt(texto)       # guardamos texto


    def getRoot(self):
        r"Devuelve el padre del elemento actual."
        return self.root



    # Parámetros por tag
    def importCSV(self, file):
        # Leemos el csv
        with open(file, newline='') as f:
            reader = csv.reader(f)
            next(reader)                # Nos saltamos el encabezado
            filas = list(reader)

        listaDeTagsPersonalizados = []
        filasDesglosadas = []
        for fila in filas:
            r"""Recorremos el archivo desenvolviendo aquellos tags que comparten
            propiedades para hacer más fácil su procesado posterior.
            Consume mucha más memoria."""
            tags = fila[0].split('|')
            for tag in tags:
                nuevaFila = [tag, fila[1], fila[2], fila[3]]
                listaDeTagsPersonalizados.append( tag )
                filasDesglosadas.append( nuevaFila )
        return listaDeTagsPersonalizados, filasDesglosadas
