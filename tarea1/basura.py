# basura

 




# Para visualizar el DOM analizado
def addNodo(grafo, nodo):
    idNodo = f'{nodo.nombre}_{nodo.uid}'
    # Por defecto queremos rojo las cajas de texto y azul lo demás
    colorNodo = 'red' if idNodo in ['div', 'p', 'span', 'h1'] else 'blue'
    
    # Creamos nodo
    grafo.add_node(idNodo, color=colorNodo)

    # Personalizamos según los atributos o no
    if len(nodo.atributos) > 0 :
        for att in nodo.atributos:
            match att[0]:
                case 'id':  # Añadimos id
                    grafo.add_node(idNodo, id=att[1])
                case 'style': 
                    estilos = att[1].split(';')
                    for estilo in estilos:
                        if estilo.startswith('color'):  # Cambiamos color
                            colorDeForma = estilo.split(':')[1].strip()
                            grafo.add_node(idNodo, color=colorDeForma)
                case 'src':  # Muestra la imagen
                    grafo.add_node(idNodo, image=att[1])
                case _:
                    print(f'Atributo desconocido: {att[0]}->{att[1]}')
                    pass
        #print(' '*profundidad + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}')
        pass
    else:
        #print(' '*profundidad + f'{ele.nombre}: {ele.txt}')
        pass
    
    # Si tiene texto lo añadimos como label. Podríamos añadir un nodo hijo con forma plaintext
    if len(nodo.txt) > 0:
        idNodoTexto = f'{nodo.txt}_{nodo.uid}'
        grafo.add_node(idNodoTexto, shape='plaintext')
        grafo.add_edge(idNodo, idNodoTexto)

    # recorremos los hijos de forma recursiva
    for hijo in nodo.hijos:
        addNodo(grafo, hijo)
        idNodoHijo = f'{hijo.nombre}_{hijo.uid}'
        grafo.add_edge(idNodo, idNodoHijo)
    

def generarGraphml(DOM):
    #G = nx.Graph()                      # crear un grafo
    #G.__setattr__("charset", "UTF-8")
    #addNodo(G, DOM)                     # creamos recursivamente nodos a partir del nodo raíz
    #nx.write_graphml(G, "prueba.graphml")
                                        # escribimos archivo de salida
    #nx.write_latex(G, "prueba.latex")                                

    #A = nx.nx_agraph.to_agraph(G)
    #A.layout('dot')
    #A.draw('salida.png') # guardar como png
    pass
    

def addNodoG(nodo):
    grafo = ''
    idNodo = f'{nodo.nombre}_{nodo.uid}'
    
    # Por defecto queremos rojo las cajas de texto y azul lo demás
    colorNodo = 'red' if idNodo in ['div', 'p', 'span', 'h1'] else 'blue'
    nodo.atributos.append(('color', colorNodo))

    for att in nodo.atributos:
        print(att)
    #atributos.append(f'color={colorNodo}')
    
    # Personalizamos según los atributos o no
    if len(nodo.atributos) > 0 :
        for att in nodo.atributos:
            match att[0]:
                case 'id':  # Añadimos id
                    #grafo.add_node(idNodo, id=att[1])
                    pass
                case 'style': 
                    estilos = att[1].split(';')
                    for estilo in estilos:
                        if estilo.startswith('color'):  # Cambiamos color
                            colorDeForma = estilo.split(':')[1].strip()
                            #grafo.add_node(idNodo, color=colorDeForma)
                case 'src':  # Muestra la imagen
                    #grafo.add_node(idNodo, image=att[1])
                    pass
                case _:
                    #print(f'Atributo desconocido: {att[0]}->{att[1]}')
                    pass
        #print(' '*profundidad + f'{ele.nombre} [{list2str(ele.atributos)}]: {ele.txt}')
        pass
    else:
        #print(' '*profundidad + f'{ele.nombre}: {ele.txt}')
        pass

    # Creamos nodo
    #grafo.add_node(idNodo, color=colorNodo)

    # Si tiene texto lo añadimos como label. Podríamos añadir un nodo hijo con forma plaintext
    nodo.atributos.append(('label', nodo.txt if len(nodo.txt)>0 else nodo.nombre))
    '''
    if len(nodo.txt) > 0:
        nodo.atributos.append(('label', nodo.txt))
    else:
        nodo.atributos.append(('label', nodo.nombre))
    '''

    # Generación Graph.dot
    grafo += f'{idNodo} [{getAtributos(nodo.atributos)}]\n'

    

    # recorremos los hijos de forma recursiva
    for hijo in nodo.hijos:
        grafo += addNodoG(hijo)
        idNodoHijo = f'{hijo.nombre}_{hijo.uid}'
        #grafo.add_edge(idNodo, idNodoHijo)
        grafo += addEdgeG(idNodo, idNodoHijo)

    return grafo

def addEdgeG(nodo, hijo):
    return f'{nodo}->{hijo}\n'

def encabezado():
    match tipoDeGrafico:
        case 'dot':
            return '''digraph G {
  charset="UTF-8"
  '''
        case _:
            raise Exception('Tipo de gráfico NO válido')

def cierre():
    match tipoDeGrafico:
        case 'dot':
            return '}'
        case _:
            raise Exception('Tipo de gráfico NO válido')


def getAtributos(atributos):
    salida = ''
    for att in atributos:
        salida += f'{att[0]}="{att[1]}"\n'
    return salida
  