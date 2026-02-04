<?php
/* ==============================
   CONEXIÓN
   ============================== */
%%COLUMNAS_DEF%%

$env = parse_ini_file(__DIR__ . "/.env");

if ($env === false) {
    die("No se pudo leer el fichero .env");
}

$host = $env["HOST"];
$db   = $env["DB"];
$user = $env["USER"];
$pass = $env["PASS"];

try {
    $pdo = new PDO(
        "mysql:host=$host;dbname=$db;charset=utf8mb4",
        $user,
        $pass,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
} catch (PDOException $e) {
    die("Error de conexión: " . $e->getMessage());
}


/* ==============================
   CREATE
   ============================== */

if (isset($_POST["create"])) {

    $stmt = $pdo->prepare(
        "INSERT INTO %%TABLA_NOMBRE%% (%%NOMBRES_DE_CAMPOS%%)
         VALUES (%%BIND_CAMPOS%%)"
    );

    $stmt->execute([
%%POST_CAMPOS%%
    ]);
}


/* ==============================
   UPDATE
   ============================== */

if (isset($_POST["update"])) {

    $stmt = $pdo->prepare(
        "UPDATE %%TABLA_NOMBRE%%
         SET %%UPDATE_BIND_CAMPOS%%"
    );

    $stmt->execute([
%%POST_UPDATE_CAMPOS%%
    ]);
}


/* ==============================
   DELETE
   ============================== */

if (isset($_POST["delete"])) {

    $stmt = $pdo->prepare(
        "DELETE FROM %%TABLA_NOMBRE%% WHERE %%CAMPO_KEY%% = ?"
    );

    $stmt->execute([$_POST["%%CAMPO_KEY%%"]]);
}


/* ==============================
   READ
   ============================== */

$filas = $pdo->query(
    "SELECT * FROM %%TABLA_NOMBRE%% ORDER BY id"
)->fetchAll(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>CRUD %%TABLA_NOMBRE%%</title>
<style>
    body { font-family: Arial, sans-serif; }
    section { border:1px solid #999; padding:15px; margin-bottom:20px; }
</style>
</head>
<body>

<h1>CRUD tabla %%TABLA_NOMBRE%%</h1>

<!-- ===================================================== -->
<!-- CREATE -->
<!-- ===================================================== -->

<section>
<h2>CREATE – Alta de %%TABLA_NOMBRE%%</h2>

<form method="post">
%%FORM_CREATE_CAMPOS%%
    <button type="submit" name="create">Crear</button>
</form>
</section>


<!-- ===================================================== -->
<!-- READ -->
<!-- ===================================================== -->

<section>
<h2>READ – Listado de %%TABLA_NOMBRE%%</h2>

<table border="1">
<tr>
%%READ_COLUMNS%%</tr>

<?php foreach ($filas as $fila): ?>
<tr>
%%READ_DATOS%%</tr>
<?php endforeach; ?>

</table>
</section>


<!-- ===================================================== -->
<!-- UPDATE -->
<!-- ===================================================== -->

<section>
<h2>UPDATE – Modificar %%TABLA_NOMBRE%%</h2>

<form method="post">
%%FORM_CREATE_CAMPOS%%
    <button type="submit" name="update">Actualizar</button>
</form>
</section>


<!-- ===================================================== -->
<!-- DELETE -->
<!-- ===================================================== -->

<section>
<h2>DELETE – Borrar %%TABLA_NOMBRE%%</h2>

<form method="post">
    ID del alumno:
    <input type="number" name="id" required>

    <button type="submit" name="delete">Eliminar</button>
</form>
</section>

</body>
</html>
