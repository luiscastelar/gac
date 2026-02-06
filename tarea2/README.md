# Lo hecho
1. Inferencia de tipo de archivo de entrada
2. Inferencia de sistema gestor
3. Utilización del sistema gestor como herramienta de obtención de metadatos más fiable que el procesado del script SQL
4. Infraestructura de contenedores para sistemas gestores (mariadb, sqlite, etc), así como motores de renderizado de salida (php, etc.)
5. Generación de la salida y conexión automática al sistema gestor de prueba. Con sustituir el fichero .env podemos conectarnos a otro servidor del mismo tipo de sistema gestor.
6. Plantillas ampliables para entradas (consultas preformadas) y salidas ("pantallas" preformadas)
7. Si se gestionan los atributos obligatorios mediante el empleo de "required"
8. Si se gestionan las actualizaciones y borrados de los tablas vinculadas mediante "ON DELETE CASCADE ON UPDATE CASCADE"

# Lo obviado
El motivo de este trabajo es la generación automática de código por lo que se han obviado los siguientes conceptos:
1. Seguridad: para su utilización real se debería establecer un mecanismo de autenticación para el acceso a la base de datos, o si estamos generando una herramienta abierta, el usuario deberá proporcionar las credenciales.
2. A prueba de fallos: existen múltiples consultas que pueden arrojar excepciones que detienen la aplicación y deberían ser adecuadamente atrapadas y procesadas.
3. No gestiono los ID. Esto es, el usuario debe indicar un ID que no existe para CREAR, o uno que existe para MODICAR o ELIMINAR
4. No gestiono los Foreign Key de las tablas. El usuario deber crear la tabla madre antes de insertar en la tabla derivada.