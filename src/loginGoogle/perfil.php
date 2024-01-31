<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bienvenido</title>
  <link rel="stylesheet" href="../css/styles.css">
  <link rel="stylesheet" href="../css/header.css">
</head>
<body>
   <?php
  require_once ('../login-with-google.php');
?>
  <?php include '../includes/header.php'; ?>
  <div>
    <img src="imagenes/foto.png" alt="">
    <h2>Bienvenido <?php echo $name ?></h2>
    <h3><?php echo $email?></h3>
  </div>
</body>
</html>