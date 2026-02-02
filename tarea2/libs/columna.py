class Columna:

    def __init__(self, nombre):
        self.nombre = nombre
        
    def str(self):        
        txt = ""
        for prop in self.__dict__:
            if prop == 'nombre':
                txt += f'    - {prop}\n'
            else:
                txt += f'      > {prop}:{getattr(self,prop)}\n'
        return txt