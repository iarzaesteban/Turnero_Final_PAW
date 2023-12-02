<?php
$db_host = 'db_postgres';
$db_name = 'turnero_unlu';
$db_user = 'turnero_user';
$db_pass = 'turnero_password';

try {
    $hashedPassword = password_hash($db_pass, PASSWORD_BCRYPT);
    $db = new PDO("pgsql:host={$db_host};dbname={$db_name}", $db_user, $db_pass);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Error: " . $e->getMessage());
}
