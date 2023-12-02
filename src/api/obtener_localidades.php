<?php
require_once '../db/db.php';

try {
    $id_provincia = $_POST['provincia'];
    error_log("provincia es ". $id_provincia);
    $stmt = $db->prepare('SELECT id_localidad, nombre 
        FROM localidad WHERE id_provincia = ?');
    $stmt->execute([$id_provincia]);   

    $localidades = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($localidades as $localidad) {
        echo '<option value="' . $localidad['id_localidad'] . '">'
             . $localidad['nombre'] . '</option>';
    }
} catch (PDOException $e) {
    die("Error: " . $e->getMessage());
}
?>
