<?php

require_once 'configurations-google.php';
require_once 'db/db.php'; 

if (isset($_GET['code'])) {
    
    $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
    $client->setAccessToken($token["access_token"]);

    $oauthService = new Google_Service_Oauth2($client);
    $userData = $oauthService->userinfo->get();
    
    $email = $userData->email;
    $name = $userData->name;
    
  
    session_start();
    $_SESSION['name'] = $name;

    $stmt = $db->prepare("SELECT id_usuario, loggin FROM Usuario WHERE username = ?");
    $stmt->execute([$email]);
    $userExists = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$userExists) {
        $insertPersonaStmt = $db->prepare("INSERT INTO Persona (nombre, correo) VALUES (?, ?)");
        $insertPersonaStmt->execute([$name, $email]);

        $idPersona = $db->lastInsertId();

        $insertUsuarioStmt = $db->prepare("INSERT INTO Usuario (id_persona, username, loggin) VALUES (?, ?, TRUE)");
        $insertUsuarioStmt->execute([$idPersona, $email]);
        
        $_SESSION['user_id'] = $db->lastInsertId();
    }elseif (!$userExists['loggin']) {
        $updateLoginStmt = $db->prepare("UPDATE Usuario SET loggin = TRUE WHERE id_usuario = ?");
        $updateLoginStmt->execute([$userExists['id_usuario']]);
        
        $_SESSION['user_id'] = $userExists['id_usuario'];
        
        header("Location: ../home.php");
        exit();
    }else {
        $error_message = "El usuario $name ya tiene una sesión abierta.";
    }

    session_write_close();
    header("Location: ../index.php?error_message=" . urlencode($error_message));
    exit();
}
?>