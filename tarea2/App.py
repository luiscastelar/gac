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

    # DONE: 2. Carga del archivo de entrada (DDL)
    sql, tipoDB = loadDDL()

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
    #tipoSalida, indexFile = TUI.eleccionDeSalida()
    tipoSalida, indexFile = 'php', 'index.php'
    #tipoSalida, indexFile = 'python', 'crud.py'
    logging.debug(f'Tipo de salida: {tipoSalida}')
    
    # DONE: 10. Captura de config de servidor según tipo de salida
    variablesDeEntorno.update(
        Env.get(settings.TAREA_PATH + 'config/' + tipoSalida + '/config')
    )
    logging.debug(f'Datos conexión a variablesDeEntorno: {variablesDeEntorno}')

    # DONE: 11. Generación de código de salida (plantillas)
    alturaVentana = len(metadatos.tablas) * 50 + 50  # altura variable
    
    # TODO: Posible pagina índice de tablas
    plantillaIn = settings.TAREA_PATH + 'templates/' + tipoSalida + '/'
    plantillaOut = settings.TAREA_PATH + 'salida/' + tipoSalida + '/'
    plantillaBoton = File().load(plantillaIn + 'boton.template')
    botones = ''
    uiId = 1  # Identif. de elemento gráfico
    for tabla in metadatos.tablas:
        boton = plantillaBoton.replace('%%ID%%', str(uiId))
        uiId += 1
        botones += boton.replace('%%TEXTO%%', tabla.nombre)+'\n'
        print(f'-> {tabla.nombre}')
    # FIXME: VOY POR AQUÍ  -> Me genera sólo una ventana (EN PYTHON)
    ventanaMain = File().load(plantillaIn + indexFile).replace('%%BOTONES%%', botones)
    ventanaMain = ventanaMain.replace('%%ALTURA%%', str(alturaVentana))
    ventanaMain = ventanaMain.replace('%%UI_TYPE%%', tipoSalida)
    ventanaMain = ventanaMain.replace('%%TIPO_DB%%', variablesDeEntorno['TIPO_DB'])
    logging.debug(ventanaMain)
    File().save(plantillaOut + indexFile, ventanaMain)

    # TODO: Páginas individuales por tabla
    plantillaTabla = File().load(plantillaIn + 'tabla.' + tipoSalida)
    for tabla in metadatos.tablas:
        #"mysql:host=$host;dbname=$db;charset=utf8mb4",
        #$user,
        #$pass,
        #[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        pdoType = db.comandosSQL['pdo_type'].replace("%%DB%%", db.name)
        contenidoTabla = plantillaTabla.replace('%%PDO_TYPE%%', pdoType)
        contenidoTabla = contenidoTabla.replace('%%UI_TYPE%%', tipoSalida)
        contenidoTabla = contenidoTabla.replace('%%TIPO_DB%%', variablesDeEntorno['TIPO_DB'])
        contenidoTabla = contenidoTabla.replace('%%TABLA_NOMBRE%%', tabla.nombre)
        # Columnas
        nombresDeCampos = ''
        bindCampos = ''
        postCampos = ''
        formCreateCampos = ''
        readColumns = ''
        readDatos = ''
        columnaPK = None
        updateBindCampos = ''
        updatePostCampos = ''

        for columna in tabla.columnas:
            nombre = columna.COLUMN_NAME
            # Form
            dataType = db.convertDataType(columna.DATA_TYPE)
            required = 'required' if columna.IS_NULLABLE.upper() == 'NO' else ''

            # Create
            nombresDeCampos += nombre + ', '
            bindCampos += '?, '
            postCampos += f'\t$_POST["{nombre}"],\n'
            formCreateCampos += f'<div class="mb-3">\t<label class="form-label">{nombre.upper()}</label>\n<input type="{dataType}" name="{nombre}" class="form-control" {required} /></div>\n'

            # Read
            readColumns += f'\t<th>{nombre.capitalize()}</th>\n'
            readDatos += f'\t<td><?= htmlspecialchars($fila["{nombre}"]) ?></td>\n'

            # Update
            if columna.COLUMN_KEY == 'PRI':
                columnaPK = columna.COLUMN_NAME
                logging.debug(f'Columna PK detectada: {columnaPK}')
            else:
                updateBindCampos += f'{nombre} = ?, '
                updatePostCampos += f'\t\t$_POST["{nombre}"],\n'

        updateBindCampos = updateBindCampos[:-2] + f'\n\t\tWHERE {columnaPK} = ? ;'
        updatePostCampos += f'\t\t$_POST["{columnaPK}"]'

        # quitamos última coma y espacio
        nombresDeCampos = nombresDeCampos[:-2]
        bindCampos = bindCampos[:-2]
        postCampos = postCampos[:-2]

        contenidoTabla = contenidoTabla.replace('%%NOMBRES_DE_CAMPOS%%', nombresDeCampos)
        contenidoTabla = contenidoTabla.replace('%%BIND_CAMPOS%%', bindCampos)
        contenidoTabla = contenidoTabla.replace('%%POST_CAMPOS%%', postCampos)
        contenidoTabla = contenidoTabla.replace('%%FORM_CREATE_CAMPOS%%', formCreateCampos)
        contenidoTabla = contenidoTabla.replace('%%READ_COLUMNS%%', readColumns)
        contenidoTabla = contenidoTabla.replace('%%READ_DATOS%%', readDatos)
        contenidoTabla = contenidoTabla.replace('%%UPDATE_BIND_CAMPOS%%', updateBindCampos)
        contenidoTabla = contenidoTabla.replace('%%POST_UPDATE_CAMPOS%%', updatePostCampos)
        contenidoTabla = contenidoTabla.replace('%%CAMPO_KEY%%', columnaPK)

        columnasDef = f'// Tabla: {tabla.nombre}\n'
        for columna in tabla.columnas:
            columnasDef += f'//  + {columna.COLUMN_NAME} : {columna.DATA_TYPE}\n'
        contenidoTabla = contenidoTabla.replace('%%COLUMNAS_DEF%%', columnasDef)
        # Guardado
        File().save(plantillaOut + f'tabla_{tabla.nombre}.' + tipoSalida, contenidoTabla)

    # PDTE: Gestión de errores de consultas: insert, update, delete

    # Exportación para obtener una definición exacta
    # DONE: + mariaDB: env $(cat .env | xargs)  bash -c ' docker exec -i mariaDB mysqldump -u"$user" -p"$pass" "$db" > dump-$db.sql'
    # DONE: + sqlite: script bash
    if tipoSalida == 'php':
        utils.printInfo(f'Aplicación funcionando en http://localhost:{variablesDeEntorno["WWW_PORT"]}')
        varEnv = f'''HOST={variablesDeEntorno["SERVER_DB"]}
DB={variablesDeEntorno["DOCKER_DB"]}
USER={variablesDeEntorno["USER_DB"]}
PASS={variablesDeEntorno["PASS_DB"]}
TIPO_DB={tipoDB}
'''
        File().save(plantillaOut + '.env', varEnv)
        import shutil
        shutil.copytree(plantillaIn + '/css', plantillaOut + 'css', dirs_exist_ok=True)
        shutil.copytree(plantillaIn + '/js', plantillaOut + 'js', dirs_exist_ok=True)
        import os #, stat
        os.chmod(settings.TAREA_PATH + variablesDeEntorno['NAME_DB'], 0o777)
    pass

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


def loadDDL():
    # DONE: 2. Captura DDL de entrada
    txt = '''Archivos de muestra preparados:
  - dump-gac2.sql: DDL de ejemplo con tablas de alumnos, cursos y
    matrículas (MariaDB)
  - db-sqlite.sql: DDL de ejemplo con tablas de albums, artists y
    tracks (SQLite)
'''
    print(txt)
    # file = settings.TAREA_PATH + input('Selecciona el archivo SQL a analizar: ')
    file = settings.TAREA_PATH + 'ejemplos/dump-gac2.sql'
    #file = settings.TAREA_PATH + 'ejemplos/db-sqlite.sql'
    sql = File().load(file)
    # sql = File().load('')
    # print(f'Archivo sql:\n{sql}')
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
    logging.debug(f'Tipo de bbdd: {tipoDB}')

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
            from libs import mariaDB as db
        case 'sqlite':
            from libs import sqliteDB as db
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


# Autocargador de programa externo
if __name__ == "__main__":
    main()
