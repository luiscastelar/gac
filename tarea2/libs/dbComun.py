from . import utils
from . import TUI
from .baseDatos import BaseDatos
#from . import baseDatos as BaseDatos
from .tabla import Tabla
from .columna import Columna

settings = None


def getDriverDB(tipoDB):
    # DONE: 4. Importacion de driver db según tipo (DAO)
    match tipoDB:
        case 'mariadb':
            from .dbMariadb import DbMariadb as db
        case 'sqlite':
            from .dbSqlite import DbSqlite as db
        case 'oracle-xe':
            #from libs import oracleDB as db
            pass
        case _:
            utils.printError(f'Gestor de BBDD {tipoDB} no disponible', settings.EXIT['FORMAT_ERROR'])
    db = db(settings.logging)  # Instanciamos el driver de la base de datos
    #db.settings = settings  # Cargamos las variables globales en el driver que corresponda
    return db


def getConexionDB(db, variablesDeEntorno):
    # DONE: Carga de metadatos
    host = variablesDeEntorno['SERVER_DB']
    port = variablesDeEntorno['PORT_DB']
    user = variablesDeEntorno['USER_DB']
    dbName = variablesDeEntorno['NAME_DB']
    password = variablesDeEntorno['PASS_DB']
    try:
        conn = db.getConn(host, port, user, password, dbName)
    
    except Exception as e:
        print(f'Error al conectar a la base de datos: {e}')
        try:
            conn = db.getConn(host, port, user, password, None)
        except Exception as e:
            print(f'Error al conectar a la base de datos sin especificar el nombre: {e}')
            return None
    
    return conn


def generacionDeMetadatos(db):
    dbName = db.name
    print(f'Generando metadatos de la base de datos {dbName}...')
    comandosSQL = db.comandosSQL
    
    # DONE: Captura de estructura según tipo 'templates/{{dbName}}/sql'
    metadatos = BaseDatos(dbName)
    # Captura de tablas
    sql = comandosSQL['show_tables'].replace("%%DB%%", dbName)
    tablas = []
    # Lista de columnas
    atributos = ['TABLE_NAME', 'COLUMN_NAME', 'ORDINAL_POSITION', 'COLUMN_DEFAULT', 'IS_NULLABLE', 'DATA_TYPE', 'CHARACTER_MAXIMUM_LENGTH', 'NUMERIC_PRECISION', 'COLUMN_TYPE', 'COLUMN_KEY', 'COLUMN_COMMENT']
    for tab in db.readSimpleList(sql):
        nombreTabla = tab[0]
        # Captura de columnas
        sql = comandosSQL['show_columns'].replace('%%TABLA%%', nombreTabla)
        columnas = db.readSimpleList(sql)
        tabla = Tabla(nombreTabla)
        for col in columnas:
            columnaNombre = col[1]
            columna = Columna(columnaNombre)
            for i in range(0, len(col)):
                k = atributos[i]
                v = col[i]
                setattr(columna, k, v)
            tabla.columnas.append(columna)    # añadimos columna a columnas[]
        tablas.append(tabla)                  # añadimos tabla a tablas[]
    metadatos.tablas = tablas                   # añadimos tablas a db
    settings.logging.debug('Metadatos capturados:\n' + metadatos.str())
    # print(metadatos.str())
    return metadatos
