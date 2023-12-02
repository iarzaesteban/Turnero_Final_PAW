<?php

require_once 'configurations-google.php';

if (isset($_GET['code'])) {
    
    $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
    $client->setAccessToken($token["access_token"]);

    $oauthService = new Google_Service_Oauth2($client);
    $userData = $oauthService->userinfo->get();
    $email = $google_account_info->email;
    $email = $google_account_info->name;

    header('Location: index.php');
    exit();
}

?>
