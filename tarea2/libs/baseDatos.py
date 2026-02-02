class BaseDatos:
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.tablas = []


    def str(self):
        txt = f"DB: {self.nombre}. Tablas:\n"
        for tabla in self.tablas:
            txt += f'  + {tabla.str()}'
        return txt