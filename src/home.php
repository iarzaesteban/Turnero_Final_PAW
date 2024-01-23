<?php
session_start();

if (!isset($_SESSION['code'])) {
    header('Location: index.php');
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <!-- Agrega aquí tus estilos CSS si es necesario -->
</head>
<body>
    <div>
        <h1>Bienvenido, <?php echo $_SESSION['user']['name']; ?>!</h1>
        <p>¡Gracias por iniciar sesión en nuestra aplicación!</p>
        <a href="logout.php">Cerrar sesión</a>
    </div>
</body>
</html>
