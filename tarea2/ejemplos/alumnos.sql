-- Versión del servidor: 10.10.2-MariaDB-1:10.10.2+maria~ubu2204-log

CREATE TABLE IF NOT EXISTS alumnos (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(20),
  apellidos varchar(50),
  edad int,
  PRIMARY KEY  (id)
)