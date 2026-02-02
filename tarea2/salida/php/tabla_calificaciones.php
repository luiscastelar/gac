<?php
/* ==============================
   CONEXIÓN
   ============================== */

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
        "INSERT INTO alumno (nombre, email, edad)
         VALUES (?, ?, ?)"
    );

    $stmt->execute([
        $_POST["nombre"],
        $_POST["email"],
        $_POST["edad"]
    ]);
}


/* ==============================
   UPDATE
   ============================== */

if (isset($_POST["update"])) {

    $stmt = $pdo->prepare(
        "UPDATE alumno
         SET nombre = ?, email = ?, edad = ?
         WHERE id = ?"
    );

    $stmt->execute([
        $_POST["nombre"],
        $_POST["email"],
        $_POST["edad"],
        $_POST["id"]
    ]);
}


/* ==============================
   DELETE
   ============================== */

if (isset($_POST["delete"])) {

    $stmt = $pdo->prepare(
        "DELETE FROM alumno WHERE id = ?"
    );

    $stmt->execute([$_POST["id"]]);
}


/* ==============================
   READ
   ============================== */

$alumnos = $pdo->query(
    "SELECT * FROM alumno ORDER BY id"
)->fetchAll(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>CRUD alumno</title>
<style>
    body { font-family: Arial, sans-serif; }
    section { border:1px solid #999; padding:15px; margin-bottom:20px; }
</style>
</head>
<body>

<h1>CRUD tabla alumno</h1>

<!-- ===================================================== -->
<!-- CREATE -->
<!-- ===================================================== -->

<section>
<h2>CREATE – Alta de alumno</h2>

<form method="post">
    Nombre:
    <input type="text" name="nombre" required>

    Email:
    <input type="email" name="email">

    Edad:
    <input type="number" name="edad">

    <button type="submit" name="create">Crear</button>
</form>
</section>


<!-- ===================================================== -->
<!-- READ -->
<!-- ===================================================== -->

<section>
<h2>READ – Listado de alumnos</h2>

<table border="1">
<tr>
    <th>ID</th>
    <th>Nombre</th>
    <th>Email</th>
    <th>Edad</th>
</tr>

<?php foreach ($alumnos as $a): ?>
<tr>
    <td><?= htmlspecialchars($a["id"]) ?></td>
    <td><?= htmlspecialchars($a["nombre"]) ?></td>
    <td><?= htmlspecialchars($a["email"]) ?></td>
    <td><?= htmlspecialchars($a["edad"]) ?></td>
</tr>
<?php endforeach; ?>

</table>
</section>


<!-- ===================================================== -->
<!-- UPDATE -->
<!-- ===================================================== -->

<section>
<h2>UPDATE – Modificar alumno</h2>

<form method="post">
    ID del alumno:
    <input type="number" name="id" required>

    Nuevo nombre:
    <input type="text" name="nombre" required>

    Nuevo email:
    <input type="email" name="email">

    Nueva edad:
    <input type="number" name="edad">

    <button type="submit" name="update">Actualizar</button>
</form>
</section>


<!-- ===================================================== -->
<!-- DELETE -->
<!-- ===================================================== -->

<section>
<h2>DELETE – Borrar alumno</h2>

<form method="post">
    ID del alumno:
    <input type="number" name="id" required>

    <button type="submit" name="delete">Eliminar</button>
</form>
</section>

</body>
</html>
