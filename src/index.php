<?php
require_once 'includes/login_process.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="css/index.css">
</head>
<body>
    <?php include 'includes/header.php'; ?>
    <section class="login-container">
        <section class="login-container-form">
            <form action="index.php" method="post">
                <label for="username">Usuario:</label>
                <span class="login-container-span">
                    <svg class="svg-inline--fa fa-user fa-w-14" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="user" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" data-fa-i2svg=""><path fill="currentColor" d="M224 256c70.7 0 128-57.3 128-128S294.7 0 224 0 96 57.3 96 128s57.3 128 128 128zm89.6 32h-16.7c-22.2 10.2-46.9 16-72.9 16s-50.6-5.8-72.9-16h-16.7C60.2 288 0 348.2 0 422.4V464c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48v-41.6c0-74.2-60.2-134.4-134.4-134.4z"></path></svg>
                    <input type="text" id="username" name="username" required>       
                </span> 
                <br>
                <label for="password">Clave:</label>
                <span class="login-container-span">
                    <svg class="svg-inline--fa fa-key fa-w-16" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="key" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" data-fa-i2svg=""><path fill="currentColor" d="M512 176.001C512 273.203 433.202 352 336 352c-11.22 0-22.19-1.062-32.827-3.069l-24.012 27.014A23.999 23.999 0 0 1 261.223 384H224v40c0 13.255-10.745 24-24 24h-40v40c0 13.255-10.745 24-24 24H24c-13.255 0-24-10.745-24-24v-78.059c0-6.365 2.529-12.47 7.029-16.971l161.802-161.802C163.108 213.814 160 195.271 160 176 160 78.798 238.797.001 335.999 0 433.488-.001 512 78.511 512 176.001zM336 128c0 26.51 21.49 48 48 48s48-21.49 48-48-21.49-48-48-48-48 21.49-48 48z"></path></svg>
                    <input type="password" id="password" name="password" required>
                </span> 
                <br>
                <button type="submit">Login</button>
                <?php require ('login-with-google.php') ?>
                <section class="login-container-form-footer">
                    <a href="<?php echo $client->createAuthUrl() ?>" >Iniciar sesión con Google</a>
                    <a href="signup.php">Crear Usuario</a>
                </section>
                <?php if (isset($error_message)) : ?>
                    <p class="error"><?php echo $error_message; ?></p>
                <?php endif; ?>
            </form>
        </section>
    </section>
    <?php include 'includes/footer.php'; ?>
</body>
</html>



