from .dbTipo import DbTipo
import os
import sqlite3


class DbSqlite(DbTipo):
    def __init__(self, logging=None):
        super().__init__(logging)
        self.TAREA_PATH = os.path.dirname(__file__)[:-5] + '/'  # Ruta del proyecto


    def getConn(self, host='sqlite-gap2.db', port=None, user=None, password=None, dbName=None):
        """Estandarizamos la conexión a bbdd

        :param host: Host de la base de datos
        :param port: no procede
        :param user: no procede
        :param password: no procede
        :param dbName: no procede
        :return: Conexión a la base de datos
        """
        self.fileDB = self.TAREA_PATH + host
        print(f"Conectando a la base de datos SQLite en '{self.fileDB}'...")
        self.conn = sqlite3.connect(self.fileDB)
        self.name = host
        return self.conn
    

    def dropDB(self):    
        """
        Elimina una base de datos si existe.

        :return: False si no se ha podido eliminar la base de datos, True si se ha eliminado correctamente
        """
        error = False
        try:
            from pathlib import Path
            Path.unlink(self.fileDB)
            self.printInfo(f'BBDD eliminada')

        except sqlite3.Error as err:
            self.printError(f"Error al eliminar la base de datos '{self.name}': {err}")
            error = True

        return True if not error else False


    def createDB(self, dbName):
        """
        Crea una base de datos si no existe.

        :param dbName: nombre de la base de datos
        :return: La conexión actual (para el caso de SQLite)
        """

        conexion = self.getConn(self.name, None, None, None)
        if conexion != None:
            print(f'BBDD "{self.name}" creada nuevamente')
            return conexion
        else:
            print(f'Problemas creando la "{self.name}"')
        return None
    

    def loadFromSQL(self, sql):
        """
        Ejecuta un fichero SQL completo (DDL + DML) sobre una conexión MySQL.

        :param sql: contenido del fichero sql
        :return: False si no se ha podido ejecutar el script SQL, True si se ha ejecutado correctamente
        """
        cursor = self.conn.cursor()
        error = False
        try:
            cursor = self.conn.cursor()
            cursor.executescript(sql)        
            self.printInfo(f"Script sql ejecutado correctamente.")

        except sqlite3.Error as err:
            self.conn.rollback()
            self.printError(f"Error ejecutando el script SQL: {err}")
            error = True

        finally:
            cursor.close()
        
        if error:
            raise Exception("Error ejecutando el script SQL")
        else:
            return True


    def readSimpleList(self, sql:str )->list[list[str]]:
        """
        Select ... -> lista (filas) de listas (columnas)
        
        :param sql: consulta SQL a ejecutar
        :type sql: str
        :return: lista de listas con los resultados de la consulta SQL
        :rtype: list[list[str]]
        """
        listOfTuples = self.read(sql)
        salida = []
        for fila in listOfTuples:
            arrayFila = []
            for ele in fila:
                arrayFila.append(ele)
            salida.append(arrayFila)
        return salida


    def convertDataType(self, tipo:str )->str:
        """
        Convierte un tipo de dato SQL a un tipo de dato Python.
        
        :param tipo: tipo en SQL a convertir
        :type tipo: str
        :return: tipo de dato en Python equivalente al tipo de dato SQL proporcionado
        :rtype: str
        """
        match(tipo):
            case 'int':
                return 'number'
            case 'varchar':
                return 'text'
            case _:
                return 'text'


    def read(self, sql):
        """
        Devuelve todas las filas
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.printInfo(f'Lectura {sql} correcta')
            return cursor.fetchall()
        finally:
            cursor.close()
