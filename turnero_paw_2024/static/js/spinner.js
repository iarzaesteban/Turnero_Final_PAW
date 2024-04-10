document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('send-email-form');
    const sendEmailBtn = document.getElementById('send-email-form__btn');
    const spinner = document.getElementById('spinner');
    const textButton = document.getElementById('text-btn');

    function areFieldsFilled() {
        const email = form.querySelector('input[name="email"]').value.trim();
        const subject = form.querySelector('input[name="subject"]').value.trim();
        const message = form.querySelector('textarea[name="message"]').value.trim();
        return email !== '' && subject !== '' && message !== '' && validateEmailFormat(email);
    }

    spinner.classList.add("spinner-hidden");

    function validateEmailFormat(email) {
        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regexEmail.test(email);
    }

    sendEmailBtn.addEventListener('click', function() {
        if (areFieldsFilled()) {
            textButton.style.display = "none";
            spinner.classList.remove("spinner-hidden");
        }
    });
});
