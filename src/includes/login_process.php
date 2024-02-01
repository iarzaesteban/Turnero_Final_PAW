<?php
require_once 'db/db.php';

session_start();

if (isset($_SESSION['google_user'])) {
    unset($_SESSION['google_user']);
}

function isUserAlreadyLoggedIn($username, $db) {
    $user = $db->prepare("SELECT loggin FROM Usuario WHERE username = ?");
    $user->execute([$username]);
    return $user->fetch(PDO::FETCH_ASSOC)['loggin'];
}

function loginUser($username, $password, $db) {
    $stmt = $db->prepare("SELECT id_usuario, username, password_hash, loggin 
        FROM Usuario WHERE username = ?");
    $stmt->execute([$username]);

    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && !$user['loggin'] && password_verify($password, $user['password_hash'])) {
        $_SESSION['user_id'] = $user['id_usuario'];
        $_SESSION['username'] = $user['username'];

        $updateStmt = $db->prepare("UPDATE Usuario SET loggin = TRUE WHERE id_usuario = ?");
        $updateStmt->execute([$user['id_usuario']]);

        return true;
    }

    return false;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if (loginUser($username, $password, $db)) {
        header('Location: home.php');
        exit();
    } else {
        if (isUserAlreadyLoggedIn($username, $db)) {
            $error_message = "El usuario $username ya tiene una sesión abierta.";
        } else {
            $error_message = "Usuario o contraseña incorrectos.";
        }
    }
}

?>
