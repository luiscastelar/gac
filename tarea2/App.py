# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------
from libs.Env import Env
from libs.contentOfFile import File
import libs.TUI as TUI
import libs.utils as utils
import settings
from libs.baseDatos import BaseDatos
from libs.tabla import Tabla
from libs.columna import Columna

# ---------------------------------------------------------------------
# Variables globales
# ---------------------------------------------------------------------
logging = None

# ---------------------------------------------------------------------
# Main()
# ---------------------------------------------------------------------
def main():
    global logging
    
    # DONE: 1. Iniciazilación de variables globales
    logging = initGlobalSettings()
    logging.info('0. Inicio del programa')

    # DONE: 2. Carga del archivo de entrada (DDL)
    # - vacio o 0 para preguntar por consola
    # - 1 para cargar dump-gac2.sql
    # - 2 para cargar db-sqlite.sql
    sql, tipoDB = loadDDL(1)

    # DONE: 3. Carga de variables de entorno comunes a todos los tipos de salida
    variablesDeEntorno = loadEnvironmentVar(tipoDB)

    # DONE: 4. Carga driver
    db = getDriverDB(tipoDB)

    # DONE: 5. Comandos "normalizados" vía plantilla
    db.comandosSQL = Env.get(settings.TAREA_PATH + 'templates/' + tipoDB + '/sql')

    # DONE: 6. Import en db pruebas
    db.conn = getConexionDB(db, variablesDeEntorno)

    # DONE: 7. Importar datos
    db.name = variablesDeEntorno['NAME_DB']
    db.loadFromSQL(db.conn, db.name, sql)

    # DONE: 8. Generación de metadatos
    metadatos = generacionDeMetadatos(db)

    # DONE: 9. Eleccion de salida
    # - vacio o 0 para preguntar por consola
    # - 1 para salida python
    # - 2 para salida php
    tipoSalida, indexFile = TUI.eleccionDeSalida(1)
    variablesDeEntorno.update({
        'tipoSalida': tipoSalida,
        'indexFile': indexFile
    })
    logging.debug(f'Tipo de salida: {tipoSalida}')
    
    # DONE: 10. Captura de config de servidor según tipo de salida
    variablesDeEntorno.update(
        Env.get(settings.TAREA_PATH + 'config/' + tipoSalida + '/config')
    )
    
    logging.debug(f'Datos conexión a variablesDeEntorno: {variablesDeEntorno}')

    # DONE: 11. Importacion de driver salida según tipo (DAO)
    out = getDriverSalida(tipoSalida)
    out.settings = settings
    out.logging = logging

    # TODO: 12. Generar indice de tablas
    out.generarIndex(metadatos, variablesDeEntorno)

    # TODO: 13. Generar CRUDs individuales por tabla
    for tabla in metadatos.tablas:
        out.generarCRUD(tabla, db, variablesDeEntorno)

    # TODO: 14. Construir APP de salida (en php, python, etc.) con plantilla común y fragmentos por tabla
    out.buildApp(variablesDeEntorno)

    # PDTE: 15. Gestión de errores de consultas: insert, update, delete
    

# ----------------------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------------------
def initGlobalSettings():
    # DONE: 1. Cargamos las variables globales en settings
    logging = settings.logging
    TUI.settings = settings
    utils.settings = settings
    logging.debug('Variables globales cargadas en settings')
    return logging


def loadDDL(tipo=0):
    # DONE: 2. Captura DDL de entrada
    txt = '''Archivos de muestra preparados:
  - ejemplos/dump-gac2.sql: DDL de ejemplo con tablas de alumnos, cursos y matrículas (MariaDB)
  - ejemplos/db-sqlite.sql: DDL de ejemplo con tablas de albums, artists y tracks (SQLite)
'''
    print(txt)
    match tipo:
        case 0:
            file = settings.TAREA_PATH + input('Selecciona el archivo SQL a analizar: ')
        case 1:
            file = settings.TAREA_PATH + 'ejemplos/dump-gac2.sql'
        case 2:
            file = settings.TAREA_PATH + 'ejemplos/db-sqlite.sql'
    sql = File().load(file)
    if len(sql) > 0:
        print(f'1. Archivo {file} cargado correctamente.')
    else:
        utils.printError('Error cargando sql', settings.EXIT['NOT_FOUND'])

    r'''# Para ampliaciones:
    # DONE: Intento de inferencia de tipo de DDL
    extensonDelArchivo = pathlib.Path(file).suffix
    logging.debug( extensonDelArchivo )
    # DONE: Tipo de DDL (sql, json schema, dbml)
    tipoDDL = TUI.getTypeDDL(extensonDelArchivo)
    logging.debug(f'Tipo de entrada: {tipoDDL}')
    '''

    # DONE: Intentar inferencia de tipo de BBDD (mariadb, sqlite, oracledb,...)
    tipoDB = TUI.getTipoDB(sql)
    logging.info(f'Tipo de bbdd: {tipoDB}')

    return sql, tipoDB


def loadEnvironmentVar(tipoDB: str)->dict:
    # DONE: 3. Captura de variables de entorno comunes a todos los tipos de salida
    variablesDeEntorno = {}
    variablesDeEntorno['TIPO_DB'] = tipoDB
    variablesDeEntorno.update(
        Env.get(settings.TAREA_PATH + 'config/' + tipoDB + '/config')
    )
    logging.debug(f'Datos conexión a variablesDeEntorno: {variablesDeEntorno}')
    if len(variablesDeEntorno) > 0:
        print(f'2. Tipo {tipoDB} procesado y datos de conexión recibidos')
    else:
        utils.printError('Error datos de conexion', settings.EXIT['NOT_FOUND'])
    return variablesDeEntorno


def getDriverDB(tipoDB):
    # DONE: 4. Importacion de driver db según tipo (DAO)
    match tipoDB:
        case 'mariadb':
            from libs import dbMariadb as db
        case 'sqlite':
            from libs import dbSqlite as db
        case 'oracle-xe':
            from libs import oracleDB as db
        case _:
            utils.printError(f'Gestor de BBDD {tipoDB} no disponible', settings.EXIT['FORMAT_ERROR'])

    db.settings = settings  # Cargamos las variables globales en el driver que corresponda
    return db


def getConexionDB(db, variablesDeEntorno):
    # DONE: Carga de metadatos
    host = variablesDeEntorno['SERVER_DB']
    port = variablesDeEntorno['PORT_DB']
    user = variablesDeEntorno['USER_DB']
    dbName = variablesDeEntorno['NAME_DB']
    password = variablesDeEntorno['PASS_DB']
    conn = db.getConn(host, port, user, password)
    
    ope = TUI.operacionesDeImportacion()
    if ope <= 0:
        utils.printError(f'Operación {ope} sobre db no disponible', 1)
    if ope == 1:
        db.dropDB(conn, dbName)
    if ope <= 2:
        conn = db.createDB(conn, dbName)
    if ope <= 3:
        pass
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
    for tab in db.readSimpleList(db.conn, sql):
        nombreTabla = tab[0]
        # Captura de columnas
        sql = comandosSQL['show_columns'].replace('%%TABLA%%', nombreTabla)
        columnas = db.readSimpleList(db.conn, sql)
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
    logging.debug('Metadatos capturados:\n' + metadatos.str())
    # print(metadatos.str())
    return metadatos


def getDriverSalida(tipoSalida):
    # DONE: 11. Importacion de driver salida según tipo (DAO)
    match tipoSalida:
        case 'php':
            from libs import phpSalida as salida
        case 'python':
            from libs import pythonSalida as salida
        case _:
            utils.printError(f'Gestor de BBDD {tipoSalida} no disponible', settings.EXIT['FORMAT_ERROR'])

    salida.settings = settings  # Cargamos las variables globales en el driver que corresponda
    return salida


# Autocargador de programa externo
if __name__ == "__main__":
    main()
