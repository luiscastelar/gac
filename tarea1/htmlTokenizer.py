import logging
import re 


SEPARADORES = (' ', '<', '>', '</', '/>')
COMENTARIOS = ('<!--', '-->')
DOCTYPE = '<!DOCTYPE'

class HtmlTokenizer():
    posicionActual = 0
    tokens = []

    def parse(self, html: str):
        # Preparamos el contenido:
        #  - Eliminamos líneas ne blanco
        #  - Borramos comentarios (versión inicial)
        #  - Saltamos el Doctype, si existe
        html = html.replace('\n','')
        html = self.borrarComentarios(html)
        pos = self.saltarDOCTYPE(html)
        
        #pos = self.saltarComentarios(pos, html)  # no es necesario ya que ya lo borramos antes
        # Cargamos la etiqueta html
        pos = self.capturaTag(pos, html)
        logging.debug(f'Análisis por carácter {pos}')
                
        
    
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
            logging.debug('El archivo no tiene !DOCTYPE\n---')
        finally:
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
            logging.debug('Comentario: ' + tempExt)
        except:
            logging.debug('El archivo no tiene mas comentrios\n---')
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
                logging.debug('Comentario eliminado: ' + 
                      html[tieneComentarioEnPos:tieneComentarioEnPos+posFin])
                html = html[:tieneComentarioEnPos] + html[tieneComentarioEnPos+posFin:]

                # Actualizamos puntero
                pos = posFin

        # Retornamos html limpio
        return html
    

    def capturaTag(self, pos: int, html: str) -> int:
        # Captura los tags
        # Quizás en un futuro podríamos capturar los atributos de forma similar
        tagAperturaInicio = 0
        tagAperturaFin = 0
        contenidoInicio = 0
        contenidoFin = 0
        tagCierreInicio = 0
        tagCierreFin = 0
        posicionInterior = 0

        logging.debug(f'Vamos a procesar el trozo: ... {html[pos:pos+60].strip()} ...')
        try:
            
            temp = html[pos:].strip()
            tagAperturaInicio = temp.index(SEPARADORES[1])
            tagAperturaFin = temp.index(SEPARADORES[2])

            if tagAperturaInicio != 0:
                return pos + self.capturaTag(0, temp[:tagAperturaInicio-1])

            # Capturamos el nombre del tag
            match = re.search('\\s|>', temp[tagAperturaInicio+1:])
            finNombreTag = match.start()+1
            nombreTag = temp[tagAperturaInicio+1:tagAperturaInicio+finNombreTag]

            # Capturamos los atributos del tag
            # --- para un futuro ---

            # Es un tag autocerrado?
            pattern = '<(.|\\s)+?/>'
            tempTag = temp[tagAperturaInicio:tagAperturaFin+1]
            match = re.search(pattern, tempTag)
            if match != None:
                # Es un tag autocerrado -> no puede contener mas tags ni texto
                logging.debug(f'Tag auto-cerrado: {nombreTag}')
                #tagCierreFin = tagAperturaFin
                return pos + tagAperturaFin + 2
        
            # Buscamos el cierre
            patron = f'</\\s*{nombreTag}\\s*>'
            match = re.search(patron, temp[tagAperturaInicio:])
            tagCierreInicio,tagCierreFin = match.span()
            contenidoInicio = tagAperturaFin + 1
            tagApertura = temp[tagAperturaInicio:tagAperturaFin+1].strip()
            contenidoFin = tagCierreInicio
            tempContenido = temp[contenidoInicio:contenidoFin].strip()
            tempCierre = temp[tagCierreInicio:tagCierreFin].strip()

            logging.debug(f'''---
                          Tag apertura: {tagApertura}
                            Nombre del tag: {nombreTag}
                            Contenido: {tempContenido}
                            Tag cierre: {tempCierre}
            ''')
            longitudTotal = self.len(tempContenido)
            while posicionInterior < longitudTotal:               
                posicionInterior = self.capturaTag(posicionInterior, tempContenido)
        except:
            logging.debug(f'Sólo contenido: {html}\n')
            return self.len(html)
            pass
        return pos+tagAperturaInicio+tagCierreFin+1