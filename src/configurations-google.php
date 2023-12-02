<?php
require_once 'vendor/autoload.php';

$clientID = '26181589147-1kaqrtobg06kbkg64ip58al22piljnpl.apps.googleusercontent.com';
$clientSecret = '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';
$redirectUri = 'http://localhost:8080/loginGoogle/perfil.php';


$client = new Google_Client();
$client->setClientId($clientID);
$client->setClientSecret($clientSecret);
$client-> setRedirectUri($redirectUri);
$client->addScope("email");
$client->addScope("profile");


?>

