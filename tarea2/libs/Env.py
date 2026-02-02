from contentOfFile import File
import os

__all__ = ['Env']

class Env():

    

    def get(ruta) -> list[dict]:
        #print( os.listdir(ruta) )

        archivoEnv = File().load(ruta)

        variablesDeEntorno = {}
        for linea in archivoEnv.split('\n'):
            pares = linea.split('=')
            if len(pares) >= 2:
                key = pares[0]
                value = pares[1]
            #print(f'L: {key} -> {value}')
            variablesDeEntorno[key] = value
        return variablesDeEntorno