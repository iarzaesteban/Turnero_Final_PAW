<?php
  require_once ('../login-with-google.php');

  if ($error_message == "") {
      header("Location: ../home.php");
      exit();
  } else {
      header("Location: ../index.php");
      exit();
  }
?>