<?php

require_once 'configurations-google.php';

if (isset($_GET['code'])) {
    
    $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
    $client->setAccessToken($token["access_token"]);

    $oauthService = new Google_Service_Oauth2($client);
    $userData = $oauthService->userinfo->get();
    
    $email = $userData->email;
    $name = $userData->name;
    
}

?>
