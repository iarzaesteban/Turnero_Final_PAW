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
        <!-- <h1>Bienvenido, <?php echo $_SESSION['user']['name']; ?>!</h1> -->
        <h1>Bienvenido!</h1>
        <p>¡Gracias por iniciar sesión en nuestra aplicación!</p>
        <a href="logout.php">Cerrar sesión</a>
    </section>
    <?php include 'includes/footer.php'; ?>
</body>
</html>
