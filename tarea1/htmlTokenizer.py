#import re 

SEPARADORES = (' ', '<', '>', '</' '/>')
COMENTARIOS = ('<!--', '-->')
DOCTYPE = '<!DOCTYPE'

class HtmlTokenizer():
    posicionActual = 0
    tokens = []

    def parse(self, html: str):
        #self.tokens = re.findall("<_*(\w*)", str(html))


        # Recorremos toda la entrada
        longitudTotal = self.len(html)
        pos = self.saltarDOCTYPE(html)
        
        while pos < longitudTotal:
            pos = self.saltarComentarios(pos, html)
            pos = self.capturaTag(pos, html)
            print(f'Análisis por carácter {pos}')

            
        print(html[pos:].strip())

        
        quit(1)




    # Evita errores de tipos
    def len(self,html):
        try: 
            return len(html)
        except:
            return 0 

    # Busca DOCTYPE y lo salta
    def saltarDOCTYPE(self, html:str) -> int:
        pos = 0
        # Buscamos !DOCTYPE
        try:
            tieneDOCTYPE = html[pos:].index(DOCTYPE)
            # Buscamos la posición después del cierre de la etiqueta !DOCTYPE
            pos = html[pos+tieneDOCTYPE+1:].index('>') + 2
        except:
            print('El archivo no tiene !DOCTYPE\n---')
        finally:
            #print(html[pos:])
            return pos
        
    # Ignora los comentarios
    # Quizás en un futuro podríamos guardarlos para exportarlos
    def saltarComentarios(self, pos: int, html: str) -> int:
        tieneComentarioEnPos = 0
        posFin = 0
        try:
            temp = html[pos:]
            tieneComentarioEnPos = temp.index(COMENTARIOS[0])
            tempExt = temp[tieneComentarioEnPos:]
            posFin = tempExt.index(COMENTARIOS[1]) + len(COMENTARIOS[1])
            tempExt = tempExt[:posFin]
            print('Comentario: ' + tempExt)
        except:
            #print('El archivo no tiene mas comentrios\n---')
            pass
        return pos+tieneComentarioEnPos+posFin
    
    # Captura los tags
    # Quizás en un futuro podríamos capturar los atributos de forma similar
    def capturaTag(self, pos: int, html: str) -> int:
        inicioTagApertura = 0
        finTagApertura = 0
        inicioTagCierre = 0
        finTagCierre = 0
        try:
            temp = html[pos:]
            inicioTagApertura = temp.index(SEPARADORES[1])
            finTagApertura = inicioTagApertura + len(SEPARADORES[1])
            tempExt = temp[inicioTagApertura:]
            inicioTagCierre = temp.index(SEPARADORES[2])
            finTagCierre = inicioTagCierre + len(SEPARADORES[2])
            tempExt = tempExt[:finTagCierre]
            tempInt = tempExt[len(SEPARADORES[1]):inicioTagCierre]
            print('Tag exterior: ' + tempExt)
            print('Tag interior: ' + tempInt)

        except:
            #print('El archivo no tiene mas comentrios\n---')
            pass
        return pos+inicioTagApertura+finTagCierre