# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------
import pathlib
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


# ---------------------------------------------------------------------
# Main()
# ---------------------------------------------------------------------
def main():
    logging = settings.logging
    TUI.settings = settings
    utils.settings = settings

    # DONE: Captura de variables de entorno
    variablesDeEntorno = Env.get(settings.TAREA_PATH + settings.ENV) 
    logging.debug(f'Variables de entorno: {variablesDeEntorno}')

    # DONE: Captura de entrada
    #file = TAREA_PATH + input('Selecciona el archivo SQL a analizar: ')
    file = settings.TAREA_PATH + 'ejemplos/dump-gac2.sql'
    sql = File().load(file)
    #sql = File().load('')
    #print(f'Archivo sql:\n{sql}')
    if len(sql) > 0:
        print(f'1. Archivo {file} cargado correctamente.')
    else:
        utils.printError('Error cargando sql', settings.EXIT['NOT_FOUND'])

    # DONE: Intento de inferencia de tipo de DDL
    tipoDDL = pathlib.Path(file).suffix
    logging.debug( tipoDDL )
    # DONE: Tipo de DDL (sql, json schema, dbml)
    tipoDDL = TUI.getTypeDDL(tipoDDL)
    logging.debug(f'Tipo de entrada: {tipoDDL}')

    # DONE: Intentar inferencia de tipo de BBDD (mariadb, sqlite, oracledb,...)
    tipoDB = TUI.getTipoDB(sql)

    # DONE: Captura de config de servidor según tipo
    servidor = Env.get(settings.TAREA_PATH + 'config/' + tipoDB + '/config')
    servidor['TIPO_DB'] = tipoDB
    #settings.servidor = servidor
    logging.debug(f'Datos conexión a servidor: {servidor}')
    if len(servidor) > 0:
        print(f'2. Tipo {tipoDB} procesado y datos de conexión recibidos')
    else:
        utils.printError('Error datos de conexion', settings.EXIT['NOT_FOUND'])

    # DONE: Importacion de driver db según tipo
    match tipoDB:
        case 'mariadb':
            from libs import mariaDB as driverDB
            driverDB.settings = settings
        case 'sqlite':
            from libs import sqlite3 as driverDB
        case 'oracle-xe':
            from libs import oracle as driverDB
        case _:
            utils.printError(f'Gestor de BBDD {tipoDB} no disponible', settings.EXIT['FORMAT_ERROR'])

    # DONE: Comandos "normalizados" vía plantilla
    comandosSQL = Env.get(settings.TAREA_PATH + 'templates/' + tipoDB + '/sql')
    #print(comandosSQL)

    # DONE: Import en db pruebas
    ope = TUI.operacionesDeImportacion()    
    
    # TODO: Carga de metadatos
    host = servidor['SERVER']
    port = servidor['PORT']
    user = servidor['USUARIO']
    dbName = servidor['DB']
    password = servidor['PASS']
    conn = driverDB.getConn(host, port, user, password)
    if ope <= 0:
        utils.printError(f'Operación {ope} sobre db no disponible',1)
    if ope == 1:
        driverDB.dropDB(conn, dbName)
    if ope <= 2:
        driverDB.createDB(conn, dbName)
    if ope <= 3:
        driverDB.loadFromSQL(conn, dbName, sql)

    # TODO: Captura de estructura según tipo 'templates/{{dbName}}/sql'
    metadatos = BaseDatos(dbName)
        # Captura de tablas
    sql = comandosSQL['show_tables'].replace("%%DB%%", dbName)
    tablas = []
    for tab in driverDB.read(conn, sql):
        nombreTabla = tab.get('TABLE_NAME','-E-')
        # Captura de columnas
        sql = comandosSQL['show_columns'].replace('%%TABLA%%', nombreTabla)
        columnas = driverDB.read(conn, sql)
        tabla = Tabla(nombreTabla)
        for col in columnas:
            columnaNombre = col['COLUMN_NAME']
            columna = Columna(columnaNombre)
            for k,v in col.items():
                setattr(columna, k, v)
            tabla.columnas.append( columna )    # añadimos columna a columnas[]
        tablas.append( tabla )                  # añadimos tabla a tablas[]
    metadatos.tablas = tablas                   # añadimos tablas a db
    logging.debug('Metadatos capturados:\n' + metadatos.str())
    #print(metadatos.str())

    # TODO: Normalización de metadatos?
    #   DONE: MariaDB: "DESCRIBE alumnos" (https://www.iditect.com/faq/python/how-to-extract-table-names-and-column-names-from-sql-query-in-python.html)
    #   TODO: sqlite: "pragma table_info('albums');" (https://www.sqlitetutorial.net/sqlite-describe-table/, https://www.delftstack.com/es/howto/sqlite/sqlite-describe-table/)
    #   TODO: OracleDB: https://stackoverflow.com/questions/72883480/how-to-display-a-description-of-a-table-in-oracle-sql

    # DONE: Eleccion de salida
    tipoSalida, indexFile = TUI.eleccionDeSalida()
    logging.debug(f'Tipo de salida: {tipoSalida}')

    #   TODO: PHP
        #tipoSalida = 'php'
        #indexFile = 'index.'+tipoSalida
    #   TODO: TKINTER
        #tipoSalida = 'python'    
        #indexFile = 'CRUD.py'
    alturaVentana = len(metadatos.tablas) * 50 + 50  # altura variable por cada botón
    #   TODO: JSP

    # TODO: Posible pagina índice de tablas
    plantillaIn = settings.TAREA_PATH + 'templates/' + tipoSalida + '/'
    plantillaOut = settings.TAREA_PATH + 'salida/' + tipoSalida + '/'
    plantillaBoton = File().load(plantillaIn + 'boton.template')
    botones = ''
    uiId = 1  # Identif. de elemento gráfico
    for tabla in metadatos.tablas:                
        boton =  plantillaBoton.replace('%%ID%%', str(uiId))
        uiId += 1
        botones +=  boton.replace('%%TEXTO%%', tabla.nombre)+'\n'        
        print(f'-> {tabla.nombre}')
    #FIXME: VOY POR AQUÍ  -> Me genera sólo una ventana (EN PYTHON)
    ventanaMain = File().load(plantillaIn + indexFile).replace('%%BOTONES%%', botones)
    ventanaMain = ventanaMain.replace('%%ALTURA%%', str(alturaVentana))
    logging.debug( ventanaMain )
    File().save(plantillaOut + indexFile, ventanaMain)

    # TODO: Páginas individuales por tabla
    plantillaTabla = File().load(plantillaIn + 'tabla.' + tipoSalida)
    for tabla in metadatos.tablas:
        contenidoTabla = plantillaTabla.replace('%%TABLA_NOMBRE%%', tabla.nombre)
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
            dataType = driverDB.convertDataType(columna.DATA_TYPE)
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
    # TODO: Gestión de errores de consultas
    #  TODO: Insert que ya existe

    # TODO: Subida a bbdd de ejemplo
    # TODO: CRUD
    # TODO: DAO 
    # php
    # python
    # nodejs
    # ¿jakarta?
    # TODO: Frontend (plantillas) -> 
    # js
    # python/tkinter (https://www.youtube.com/watch?v=bwX5HnfyhfU)
    # ¿javaFX?
    # TODO: Exportación para obtener una definición exacta
    # + mariaDB: env $(cat .env | xargs)  bash -c ' docker exec -i mariaDB mysqldump -u"$user" -p"$pass" "$db" > dump-$db.sql'
    # + sqlite:
    # + oracle-xe: 
    if tipoSalida == 'php':
        utils.printInfo(f'Aplicación funcionando en http://localhost:{variablesDeEntorno["PUERTO"]}')
        varEnv = f'''
#HOST={variablesDeEntorno["host"]}
HOST=mariadb
DB={variablesDeEntorno["db"]}
USER={variablesDeEntorno["user"]}
PASS={variablesDeEntorno["pass"]}
'''
        File().save(plantillaOut + '.env', varEnv)
        import shutil
        shutil.copytree(plantillaIn + '/css', plantillaOut + 'css', dirs_exist_ok=True)
        shutil.copytree(plantillaIn + '/js', plantillaOut + 'js', dirs_exist_ok=True)
    pass





# Autocargador de programa externo
if __name__ == "__main__":
     main()
