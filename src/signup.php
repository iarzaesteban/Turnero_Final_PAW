<?php
    require_once 'includes/signup_process.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro de Usuario</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <script src="js/carga-ubicacion.js"></script>
</head>
<body>
    <div class="signup-container">
        <h2>Crear Usuario</h2>
        <form action="includes/signup_process.php" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" value="-" name="username" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" value="" name="password" required>
            <br>
            <label for="provincia">Provincia:</label>
            <select id="provincia" name="provincia" onchange="cargarLocalidades()" required>
                <!-- Aca cargamos las provincias -->
            </select>
            <br>
            <label for="localidad">Localidad:</label>
            <select id="localidad" name="localidad" required>
                <!-- Aca cargamos las localidades de acuerdo a la pcia seleccionada -->
            </select>
            <br>
            <input type="hidden" id="id_provincia" name="id_provincia">
            <button type="submit">Registrarse</button>
        </form>
        <p>¿Ya tienes una cuenta? <a href="login.php">Iniciar sesión</a></p>
    </div>
</body>
</html>

<script>
    $(document).ready(function () {
        cargarProvincias();
    });
    $("#provincia").change(function () {
        $("#id_provincia").val($(this).val());
        cargarLocalidades();
    });
</script>

