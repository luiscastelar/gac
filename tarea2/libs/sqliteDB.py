#import mysql.connector
import sqlite3

settings = None

def getConn(host, port, user, password):
    """
    Estandarizamos la conexión a bbdd.

    :param host: dirección del archivo de la bbdd
    :param port: np
    :param user: np
    :param password: np

    :return: conexión activa a la base de datos
    """
    fileDB = settings.TAREA_PATH + host
    print(f"Conectando a la base de datos SQLite en '{fileDB}'...")
    conn = sqlite3.connect(fileDB)
    return conn

def dropDB(conexion, db):    
    """
    Elimina una base de datos si existe.

    :param conexion: np
    :param db: nombre de la base de datos
    :return: conexión activa a la base de datos
    """
    try:
        from pathlib import Path
        Path.unlink(settings.TAREA_PATH + db)
        print(f'BBDD eliminada')                
    except sqlite3.Error as err:
        print(f"Error al eliminar la base de datos '{db}': {err}")


def createDB(conexion, db):
    """
    Crea una base de datos si no existe.

    :param conexion: np
    :param db: nombre de la base de datos
    """
    conexion = getConn(db, None, None, None)
    if conexion != None:
        print(f'BBDD "{db}" creada nuevamente')
        return conexion
    else:
        print(f'Problemas creando la "{db}"')

def loadFromSQL(conn, db, sql):
    """
    Ejecuta un fichero SQL completo (DDL + DML) sobre una conexión MySQL.

    :param conn: conexión activa mysql.connector
    :param sql: contenido del fichero sql
    """
    cursor = conn.cursor()

    try:
        cursor = conn.cursor()
        cursor.executescript(sql)        
        printInfo(f"Script sql ejecutado correctamente.")
    except sqlite3.Error as err:
        conn.rollback()
        print(f"Error ejecutando el script SQL: {err}")
        raise

    finally:
        cursor.close()

def read(conn, sql):
    """
    Devuelve todas las filas
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        printInfo(f'Lectura {sql} correcta')
        return cursor.fetchall()
    finally:
        cursor.close()

def readSimpleList(conn, sql):
    listOfTuples = read(conn, sql)
    salida = []
    for fila in listOfTuples:
        arrayFila = []
        for ele in fila:
            arrayFila.append(ele)
        salida.append(arrayFila)
    return salida

def convertDataType(tipo:str )->str:
    match(tipo):
        case 'int':
            return 'number'
        case 'varchar':
            return 'text'
        case _:
            return 'text'
        

def printInfo(msg):
    """
    Docstring para printInfo
    
    :param msg: texto
    """
    settings.logging.info(msg)
    print(msg)