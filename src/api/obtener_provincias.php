<?php
require_once '../db/db.php';

try {
    $stmt = $db->query('SELECT id_provincia, nombre FROM provincia');
    $provincias = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($provincias as $provincia) {
        echo '<option value="' . $provincia['id_provincia'] . '">'
             . $provincia['nombre'] . '</option>';
    }
} catch (PDOException $e) {
    die("Error: " . $e->getMessage());
}
?>
