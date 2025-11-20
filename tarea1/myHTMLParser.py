from html.parser import HTMLParser
from elemento import Elemento
import re

# Extensión de un parser sencillo
class MyHTMLParser(HTMLParser):
    root = None
    actual = None

    # Cuando encuentra un tag de apertura
    def handle_starttag(self, tag, attrs):
        # Creamos elemento
        ele = Elemento(tag)
        if self.root == None:
            # Si no existía ningún elemento lo tomamos como raíz y actual (para asignar hijos)
            self.root = ele
            self.actual = ele
        else:
            ele.asignarPadre(self.actual)    # Le asignamos el padre para recorrer hacia afuera
            self.actual.hijos.append(ele)    # Al actual le asignamos el elemento por estar anidado. Es un hijo 
            self.actual = ele                # Recorreremos el elemento en busca de hijos

        #print("Encountered a start tag:", tag)
        if len(attrs) > 0:
            #print("Atributos: " + list2str(attrs))
            ele.atributos = attrs        # guardamos la lista de atributos

    # Cuando encuentra el cierre de etiqueta
    def handle_endtag(self, tag):
        if self.actual != MyHTMLParser.root:
            # subimos al nivel superior
            self.actual = self.actual.padre
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        # Si hay texto
        if len(data.strip()) > 0:
            #print("Encountered some data  :", data)
            texto = re.sub(r'\n|\s{2,}', r' ', data)  # eliminamos saltos de página '\n' y espacios dobles
            self.actual.setTxt(texto)        # asignamos texto

    def getRoot(self):
        return self.root


