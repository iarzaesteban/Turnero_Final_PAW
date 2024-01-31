function validatePasswords() {
    // Validar coincidencia de contraseñas
    var password = document.getElementById("password").value;
    var rePassword = document.getElementById("re-password").value;
    var passwordError = document.getElementById("password-error");
    console.log("password",password)
    console.log("rePassword",rePassword)
    if (password !== rePassword) {
        passwordError.textContent = "Las contraseñas no coinciden.";
        return false; 
    } else {
        passwordError.textContent = ""; 
        return true; 
    }
}
