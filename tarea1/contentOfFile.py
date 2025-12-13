import os

__all__ = ['File']

class File():
    # Gestión de archivos

    def load(self, filepath):
        # Retorna todo el contenido del archivo o da error y finaliza programa

        if len(filepath)==0:
            # Si no se le pasa nombre lo pide
            filepath = input('Introduce el nombre del archivo (ruta completa): ')

        try: 
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f'Fallo de lectura: {e}')
            quit(2)

    
    def save(self, filepath, content):
        # Vuelca contenido en archivo o da error y finaliza programa.
        # Sobreescribe el contenido anterior

        if len(filepath)==0:
            filepath = input('Introduce el nombre del archivo (ruta completa): ')

        # Crea el directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            print(f'Write failed: {e}')
            quit(2)
        