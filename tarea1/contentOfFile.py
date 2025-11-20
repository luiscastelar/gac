import os

__all__ = ['File']

class File():

    def load(self, filepath):
        if len(filepath)==0:
            filepath = input('Introduce el nombre del archivo (ruta completa): ')

        try: 
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f'Read failed: {e}')
        #return open(nameOfFile).read()

    
    def save(self, filepath, content):        
        if len(filepath)==0:
            filepath = input('Introduce el nombre del archivo (ruta completa): ')

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            print(f'Write failed: {e}')
        