document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('confirmation-modal');

    const cancelButton = document.getElementById('cancel-button');
    const confirmButton = document.getElementById('confirm-button');
    const modalMessage = document.getElementById('modal-message');
    const acceptLinks = document.querySelectorAll('.acept-btn');
    const cancelLinks = document.querySelectorAll('.cancel-btn');
    const asignmentLinks = document.querySelectorAll('.asignment-btn');
    const finalyShiftLink = document.querySelectorAll('.finaly-shift-btn');
  
    function showModal(message) {
        modalMessage.textContent = message;
        modal.classList.add('show');
    }

    function showSpinner() {
        confirmButton.classList.add("spinner-button");
    }

    function hideSpinner() {
        spinner.style.display = 'none';
        confirmButton.disabled = false;
    }
  
    function closeModal() {
        modal.classList.remove('show');
    }

    finalyShiftLink.forEach(function(link) {
        link.addEventListener('click', function(event) {
            console.log("clickeado finally btn")
            event.preventDefault();
            showModal("¿Estás seguro de pasar este turno a estado Completado?");
            confirmButton.onclick = function() {
                window.location.href = link.href;
                
            };
        });
    });

    asignmentLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            showModal("¿Estás seguro de querer asignarte este turno?");
            confirmButton.onclick = function() {
                window.location.href = link.href;
                
            };
        });
    });
  
    acceptLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            showModal("¿Estás seguro de querer aceptar este turno?");
            confirmButton.onclick = function() {
                window.location.href = link.href;
                confirmButton.textContent = "";
                showSpinner();
                
            };
        });
    });

    cancelLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            showModal("¿Estás seguro de querer cancelar este turno?");
            confirmButton.onclick = function() {
                window.location.href = link.href;
                confirmButton.textContent = "";
                showSpinner();
                
            };
        });
    });

    if (cancelButton){
        cancelButton.addEventListener('click', function() {
            closeModal();
        });
    }
    
});
