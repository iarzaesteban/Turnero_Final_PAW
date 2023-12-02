<?php
require_once __DIR__ . '/../config.php';
require_once BASE_PATH . 'db/db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = password_hash($_POST['password'], PASSWORD_BCRYPT);
    $id_localidad = $_POST['provincia'];

    try {
        $stmt = $db->prepare('INSERT INTO persona 
            (nombre, apellido, correo, telefono, dni, id_localidad) 
                VALUES (?, ?, ?, ?, ?, ?)');
        $stmt->execute([$nombre, $apellido, $correo, $telefono, $dni, $id_localidad]);

        $id_persona = $db->lastInsertId();

        $stmt = $db->prepare('INSERT INTO usuario 
            (id_persona, username, password_hash, loggin, id_rol) 
                VALUES (?, ?, ?, ?, ?)');
        // Le asignamos un 3 al final indicando que vamos a dar de alta un cliente
        $stmt->execute([$id_persona, $username, $password, 0, 3]);

        header('Location: ../login.php');
        exit();
    } catch (PDOException $e) {
        die("Error: " . $e->getMessage());
    }
}
?>
