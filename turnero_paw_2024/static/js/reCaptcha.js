document.addEventListener('DOMContentLoaded', function() {
    grecaptcha.ready(function() {
        const form = document.getElementById('form-login');
        const recaptchaId = form.getAttribute('data-recaptcha-id');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            grecaptcha.execute('6Lc1owAqAAAAAPWgD-G3RHzmVxKMq-BwL2HxlCcs', { action: 'login' }).then(function(token) {
                document.getElementById(recaptchaId).value = token;
                event.target.submit();
            });
        });
    });
});