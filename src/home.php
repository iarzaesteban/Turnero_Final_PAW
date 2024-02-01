<?php 
    require_once('login-with-google.php'); 
    session_start();

    if (!isset($_SESSION['user_id']) && !isset($_SESSION['name'])) {
        header('Location: index.php');
        exit();
    }
    $username = $_SESSION['username'];
    $welcomeMessage = "Bienvenido " . (isset($_SESSION['name']) ? $_SESSION['name'] : $username) . " !";
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <?php include 'includes/header.php'; ?>
    <section>
        <h1><?php echo $welcomeMessage; ?></h1>
        <p>¡Gracias por iniciar sesión en nuestra aplicación!</p>
        <a href="logout.php">Cerrar sesión</a>
    </section>
    <?php include 'includes/footer.php'; ?>
</body>
</html>
