document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('form-register');

    function showSpinner() {
        const registerButton = document.getElementById('form-register__button');
        registerButton.classList.add("spinner-button");
        console.log("CLIECK desp de class BB")
    }

    registerForm.addEventListener('submit', function(event) {
        console.log("Formulario enviado");
        const registerButton = document.getElementById('form-register__button');
        registerButton.textContent = "";
        showSpinner();
    });
});