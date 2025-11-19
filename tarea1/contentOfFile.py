__all__ = ['File']

class File():

    def load(self, nameOfFile):
        if len(nameOfFile)==0:
            nameOfFile = input('Introduce el nombre del archivo (ruta completa): ')

        return open(nameOfFile).read()
    
    def save(self, nameOfFile, content):        
        if len(nameOfFile)==0:
            nameOfFile = input('Introduce el nombre del archivo (ruta completa): ')

        return open(nameOfFile,'w').write(content)
        