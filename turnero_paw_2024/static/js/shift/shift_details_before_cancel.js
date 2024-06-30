document.addEventListener('DOMContentLoaded', function() {
    const confirmationCode = JSON.parse(document.getElementById('confirmationCode').textContent);
    const cancelConfirmationButton = document.getElementById('cancel-shift-button');

    function showSpinner() {
        cancelConfirmationButton.textContent = "";
        cancelConfirmationButton.classList.add("spinner-button");
    }

    document.getElementById('cancel-shift-button').addEventListener('click', function() {
        console.log("confirmationCode", confirmationCode);
        showSpinner();
        fetch('/shift/initiate_cancel_shift/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: `confirmation_code=${confirmationCode}`
        }).then(response => response.json()).then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else if (data.success) {
                window.location.href = `/shift/confirm_cancel_shift/${data.shift_id}/`;
            }
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('Error al procesar la solicitud.');
        });
    });
    
});