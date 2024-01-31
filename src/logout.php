<?php
require_once 'db/db.php';
session_start();


if (isset($_SESSION['user_id'])) {
    $userId = $_SESSION['user_id'];
    
    $updateStmt = $db->prepare("UPDATE Usuario SET loggin = FALSE WHERE id_usuario = ?");
    $updateStmt->execute([$userId]);

    session_unset();
    session_destroy();

    header('Location: index.php');
    exit();
} else {
    header('Location: index.php');
    exit();
}
?>