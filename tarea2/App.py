from Env import Env
import os

TAREA_PATH = os.path.dirname(__file__) + '/'
MARIA_DB = 'infra/mariadb/.env'
ORACLE_DB = 'infra/oracledb/.env'
SQLITE = 'infra/sqlite/db.sqlite3'

r'''
ToDo's:
0. Selección de archivos fuente:
   0.1 DDL entrada:
      0.1.1 SQL (mariaDB, sqlite, oracle, ...) -> https://pypi.org/project/simple-ddl-parser/
         + MariaDB: SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, COLUMN_KEY FROM information_schema.columns WHERE TABLE_NAME='alumnos';
         + SQLite: 
         + OracleD: 
      0.1.2 Json Schema
      0.1.3 DBML
   0.2 XAML???
1. Intento de inferencia de tipo
   cat dump-gac2.sql | egrep -i 'mysql|mariadb' -> 0 ok y 1 NO
2. Cargar metadados de estructura
   2.1 MariaDB: "DESCRIBE alumnos" (https://www.iditect.com/faq/python/how-to-extract-table-names-and-column-names-from-sql-query-in-python.html)
   2.2 sqlite: "pragma table_info('albums');" (https://www.sqlitetutorial.net/sqlite-describe-table/, https://www.delftstack.com/es/howto/sqlite/sqlite-describe-table/)
   2.3 OracleDB: https://stackoverflow.com/questions/72883480/how-to-display-a-description-of-a-table-in-oracle-sql
3. Normalización de metadatos
4. Indice con las tablas posibles
5. CRUD - DAO (php, python, nodejs, jakarta)
6. Frontend (plantillas) -> js, python y javaFX
   6.1
   6.2 -> https://www.youtube.com/watch?v=bwX5HnfyhfU

Fuentes:
+ https://pypi.org/project/sql-metadata/
+ https://github.com/tobymao/sqlglot


Exportación para obtener una definición exacta
+ mariaDB env $(cat .env | xargs)  bash -c ' docker exec -i mariaDB mysqldump -u"$user" -p"$pass" "$db" > dump-$db.sql'
'''

def main():

   eleccion = input('Selecciona el archivo SQL a analizar')
   # ---
   # 1. Captura de sql
   # 2. Captura de config de servidor según tipo 
   # 3. Subida a bbdd de ejemplo
   # 4. Análisis de tablas show tables + describe table
   # ...
   
   variablesDeEntorno = Env.get(TAREA_PATH + MARIA_DB) 
   print(f'Variables: {variablesDeEntorno}')
   pass




# Autocargador de programa externo
if __name__ == "__main__":
     main()