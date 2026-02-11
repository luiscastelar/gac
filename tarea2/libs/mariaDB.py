import mysql.connector

settings = None
dbName = None
comandosSQL = None
conn = None

def getConn(host, port, user, password):
    "Estandarizamos la conexión a bbdd"
    if (host == 'mariadb'):
        host = 'localhost'
    conn = mysql.connector.connect(host=host, port=port, user=user, password=password)
    return conn

def dropDB(conexion, db):    
    """
    Elimina una base de datos si existe.

    :param conexion: conexión activa a MySQL
    :param db: nombre de la base de datos
    """
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{db}`;")
        conexion.commit()
        printInfo(f"Base de datos '{db}' eliminada (si existía).")

    except mysql.connector.Error as err:
        print(f"Error al eliminar la base de datos '{db}': {err}")

    finally:
        if cursor:
            cursor.close()

def createDB(conexion, db):
    """
    Crea una base de datos si no existe.

    :param conexion: conexión activa a MySQL
    :param db: nombre de la base de datos
    """
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db}` "
            "CHARACTER SET utf8mb4 "
            "COLLATE utf8mb4_unicode_ci;"
        )
        conexion.commit()
        printInfo(f"Base de datos '{db}' creada o ya existente.")
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos '{db}': {err}")

    finally:
        if cursor:
            cursor.close()

def loadFromSQL(conn, db, sql):
    """
    Ejecuta un fichero SQL completo (DDL + DML) sobre una conexión MySQL.

    :param conn: conexión activa mysql.connector
    :param sql: contenido del fichero sql
    """
    cursor = conn.cursor()

    try:
        cursor.execute(f'USE {db};')
        statement = ""
        for line in sql.splitlines():
            line = line.strip()

            # Ignorar comentarios y líneas vacías
            if not line or line.startswith("--") or line.startswith("/*"):
                continue

            statement += line + " "

            # Fin de sentencia
            if line.endswith(";"):
                cursor.execute(statement)
                statement = ""

        conn.commit()
        printInfo(f"Script sql ejecutado correctamente.")

    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error ejecutando el script SQL: {err}")
        raise

    finally:
        cursor.close()

def read(conn, sql):
    """
    Devuelve todas las filas
    """
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql)
        printInfo(f'Lectura {sql} correcta')
        return cursor.fetchall()
    finally:
        cursor.close()


def readSimpleList(conn, sql):
    lista = read(conn, sql)
    simpleList = []
    for ele in lista:
        simpleList.append(dictToList(ele))
    return simpleList


def dictToList(ele):
    lista = []
    for k, v in ele.items():
        lista.append(v)
    return lista


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