import re 

SEPARADORES = (' ', '<', '>', '</', '/>')
COMENTARIOS = ('<!--', '-->')
DOCTYPE = '<!DOCTYPE'

class HtmlTokenizer():
    posicionActual = 0
    tokens = []

    def parse(self, html: str):
        # Borramos comentarios (versión inicial)
        html = self.borrarComentarios(html)
        #print('HTML limpio:\n'+html)

        # Recorremos toda la entrada
        longitudTotal = self.len(html)
        pos = self.saltarDOCTYPE(html)
        
        while pos < longitudTotal:
            #pos = self.saltarComentarios(pos, html)  # no es necesario ya que ya lo borramos antes
            pos = self.capturaTag(pos, html)
            print(f'Análisis por carácter {pos}')
            
        print(html[pos:].strip())

        
        quit(1)

    
    def len(self,html:str) -> int:
        # Evita errores de tipos
        try: 
            return len(html)
        except:
            return 0 

    def saltarDOCTYPE(self, html:str) -> int:
        # Busca DOCTYPE y lo salta

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

    def saltarComentarios(self, pos: int, html: str) -> int:
        # Saltar comentarios
        # ToDo: 
        #  - cambiar a índices absolutos
        #  - registrar comentarios para usos futuros        
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
         
    def borrarComentarios(self, html: str)->str:  
        # Borrar comentarios del html
        # ToDo: registrarlos para usos futuros        
        longitudHtml = len(html)
        pos = 0

        # Recorremos todo eliminando los comentarios
        while pos < longitudHtml:
            # Buscamos inicio de comentario
            tieneComentarioEnPos = html.find(COMENTARIOS[0])
            if tieneComentarioEnPos == -1:
                # No quedan comentarios
                pos = longitudHtml
            else:
                # Capturamos fin del comentario, lo mostramos y lo eliminamos 
                # del texto final
                posFin = html[tieneComentarioEnPos:].find(COMENTARIOS[1]) + len(COMENTARIOS[1])
                print('Comentario eliminado: ' + 
                      html[tieneComentarioEnPos:tieneComentarioEnPos+posFin])
                html = html[:tieneComentarioEnPos] + html[tieneComentarioEnPos+posFin:]

                # Actualizamos puntero
                pos = posFin

        # Retornamos html limpio
        return html
    
    # Captura los tags
    # Quizás en un futuro podríamos capturar los atributos de forma similar
    def capturaTag(self, pos: int, html: str) -> int:
        tagAperturaInicio = 0
        tagAperturaFin = 0
        contenidoInicio = 0
        contenidoFin = 0
        tagCierreInicio = 0
        tagCierreFin = 0
        try:
            print(f'{html[pos:pos+60]}...')
            temp = html[pos:]
            tagAperturaInicio = temp.index(SEPARADORES[1])
            tagAperturaFin = temp.index(SEPARADORES[2])

            # Capturamos el nombre del tag
            match = re.search('\s|>', temp[tagAperturaInicio+1:])
            finNombreTag = match.start()+1
            nombreTag = temp[tagAperturaInicio+1:tagAperturaInicio+finNombreTag]

            # Es un tag autocerrado?
            pattern = '<(.|\s)+?/>'
            tempTag = temp[tagAperturaInicio:tagAperturaFin+1]
            match = re.search(pattern, tempTag)
            #if match.start() > -1 :
            if match != None:
                # Es un tag autocerrado -> no puede contener mas tags ni texto
                print(f'Tag auto-cerrado: {nombreTag}')
                tagCierreFin = tagAperturaFin
            else:
                # Buscamos el cierre
                patron = f'</{nombreTag}>'
                match = re.search(patron, temp[tagAperturaFin-1:])
                tagCierreInicio,tagCierreFin = match.span()
                contenidoInicio = tagAperturaFin + 1
                #tagCierreInicio = temp.index(SEPARADORES[3])  # O el '/>'
                contenidoFin = tagCierreInicio - 1            
                #tagCierreFin = temp.index(SEPARADORES[2])  # O el '/>'
                tagApertura = temp[tagAperturaInicio:tagAperturaFin+1].strip()
                tempContenido = temp[contenidoInicio:contenidoFin+1].strip()
                tempCierre = temp[tagCierreInicio:tagCierreFin+1].strip()
                print('Tag apertura: ' + tagApertura)
                print('Nombre del tag:' + nombreTag)
                print('Contenido: ' + tempContenido)
                print('Tag cierre: ' + tempCierre)
        except:
            #print('El archivo no tiene mas comentrios\n---')
            return self.len(html)
            pass
        return pos+tagAperturaInicio+tagCierreFin+1