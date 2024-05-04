document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('form-register');

    function showSpinner() {
        const registerButton = document.getElementById('form-register__button');
        registerButton.classList.add("spinner-button");
    }

    registerForm.addEventListener('submit', function(event) {
        const registerButton = document.getElementById('form-register__button');
        registerButton.textContent = "";
        showSpinner();
    });
});