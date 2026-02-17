# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------
from libs.Env import Env
from libs.contentOfFile import File
import libs.TUI as TUI
import libs.utils as utils
import settings
import libs.dbComun as dbComun

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
    db = dbComun.getDriverDB(tipoDB)

    # DONE: 5. Comandos "normalizados" vía plantilla
    db.comandosSQL = Env.get(settings.TAREA_PATH + 'templates/' + tipoDB + '/sql')

    # DONE: 6. Import en db pruebas
    db.conn = dbComun.getConexionDB(db, variablesDeEntorno)
    
    ope = TUI.operacionesDeImportacion()
    if ope <= 0:
        utils.printError(f'Operación {ope} sobre db no disponible', 1)
    if ope == 1:
        db.dropDB(db.conn, variablesDeEntorno['NAME_DB'])
    if ope <= 2:
        db.conn = db.createDB(db.conn, variablesDeEntorno['NAME_DB'])
    if ope <= 3:
        pass

    # DONE: 7. Importar datos
    db.name = variablesDeEntorno['NAME_DB']
    db.loadFromSQL(db.conn, db.name, sql)

    # DONE: 8. Generación de metadatos
    metadatos = dbComun.generacionDeMetadatos(db)

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
    dbComun.settings = settings
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
