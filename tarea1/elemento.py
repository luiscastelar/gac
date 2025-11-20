

# Clase Elemento HTML
class Elemento:
    uid = 0;

    def __init__(self, nombre):
        Elemento.uid = Elemento.uid + 1 # para evitar colisiones en los grafos
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

    def str(self):
        padre = 'self' if self.padre == None else self.padre

        return f'[nombre: {self.nombre}, padre: {padre}]'
