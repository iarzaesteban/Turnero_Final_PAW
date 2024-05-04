document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('cancel-shift-form'); 
    const modal = document.getElementById('cancel-shift-modal');
    const closeModalButton = document.getElementById('close-modal-btn');
    const cancelConfirmationButton = document.getElementById('confirm-cancel-btn');
    const descriptionTextarea = document.getElementById('cancel-description');
    const charCountElement = document.getElementById('char-count');

    descriptionTextarea.addEventListener('input', function(event) {
        const maxLength = 200;
        const textLength = descriptionTextarea.value.length; 
        const remainingChars = maxLength - textLength;

        if (textLength >= maxLength) {
            descriptionTextarea.value = descriptionTextarea.value.slice(0, maxLength);
        }
        
        charCountElement.innerHTML = `<strong>${remainingChars}</strong> caracteres restantes`;
    });

    function showModal() {
        modal.classList.add('show');
        cancelConfirmationButton.innerText = "Confirmar Cancelación";
        cancelConfirmationButton.classList.remove("spinner-button");
    }

    function closeModal() {
        descriptionTextarea.value= "";
        charCountElement.innerHTML = `<strong>200</strong> caracteres restantes`;
        modal.classList.remove('show');
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        showModal();
    });

    closeModalButton.addEventListener('click', function(event) {
        event.preventDefault();
        closeModal();
    });

    function showSpinner() {
        cancelConfirmationButton.classList.add("spinner-button");
    }

    cancelConfirmationButton.addEventListener('click', function(event) {
        event.preventDefault();
        cancelConfirmationButton.textContent = "";
        showSpinner();
        const description = descriptionTextarea.value;
        const shiftId = form.getAttribute('action').split('/').slice(-2, -1)[0]; 
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        fetch(`/shift/user-cancel-shift/${shiftId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ description: description }),
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data && data.redirect_url) {
                window.location.href = data.redirect_url;
            } else if (data && data.error_message) {
                const errorElement = document.createElement('p');
                errorElement.classList.add('error-message');
                errorElement.textContent = data.error_message;
                const containerSpan = document.getElementById('shift-details-container__span');
                const firstChild = containerSpan.firstChild;
                containerSpan.insertBefore(errorElement, firstChild);
                setTimeout(function() {
                    containerSpan.removeChild(errorElement);
                }, 10000);
            }
            closeModal();
        })
        .catch(error => {
            closeModal();
        });
    });
});
