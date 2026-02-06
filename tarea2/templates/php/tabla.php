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
    print_r($db);
    $pdo = new PDO(%%PDO_TYPE%%);
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
<link href="css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="css/default.css">
<script src="js/bootstrap.bundle.min.js"></script>
</head>
<body>
<div class="container-md py-4">
<!--
Source - https://stackoverflow.com/a/57361587
Posted by Alessio Cantarella, modified by community. See post 'Timeline' for change history
Retrieved 2026-02-04, License - CC BY-SA 4.0
-->

<div class="btn btn-success"><a href="index.php">Volver</a></div>

<h1>CRUD tabla %%TABLA_NOMBRE%%</h1>
<div class="accordion" id="crudAccordion">
    <!-- ===================================================== -->
    <!-- CREATE -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingCreate">
            <button class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseCreate">
            CRUD tabla %%TABLA_NOMBRE%%
            </button>
        </h2>

        <div id="collapseCreate"
            class="accordion-collapse collapse"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

             <form method="post">
                %%FORM_CREATE_CAMPOS%%
                <button type="submit" name="create" class="btn btn-success">Crear</button>
            </form>

            </div>
        </div>
    </div>

    <!-- ===================================================== -->
    <!-- READ -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingRead">
            <button class="accordion-button" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseRead">
            READ – Listado de %%TABLA_NOMBRE%%
            </button>
        </h2>

        <div id="collapseRead"
            class="accordion-collapse collapse show"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

            <table class="table table-striped table-bordered table-hover">
                <tr>
                %%READ_COLUMNS%%</tr>

                <?php foreach ($filas as $fila): ?>
                <tr>
                %%READ_DATOS%%</tr>
                <?php endforeach; ?>
            </table>

            </div>
        </div>
    </div>

    <!-- ===================================================== -->
    <!-- UPDATE -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingUpdate">
            <button class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseUpdate">
            UPDATE – Modificar %%TABLA_NOMBRE%%
            </button>
        </h2>

        <div id="collapseUpdate"
            class="accordion-collapse collapse"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

             <form method="post">
            %%FORM_CREATE_CAMPOS%%
                <button type="submit" name="update" class="btn btn-success">Actualizar</button>
            </form>

            </div>
        </div>
    </div>

    <!-- ===================================================== -->
    <!-- DELETE -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingDelete">
            <button class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseDelete">
            DELETE – Borrar %%TABLA_NOMBRE%%
            </button>
        </h2>

        <div id="collapseDelete"
            class="accordion-collapse collapse"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

            <form method="post">
                <label class="form-label">ID del alumno:</label>
                <input type="number" name="id" class="form-control" required>

                <button type="submit" name="delete" class="btn btn-danger">Eliminar</button>
            </form>

            </div>
        </div>
    </div>
</div>
</body>
</html>
