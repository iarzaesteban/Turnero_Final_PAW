document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const turnoModal = document.getElementById('appointmentModal');
    const turnoModalBody = document.getElementById('turno-modal-body');
    const closeModal = document.getElementById('modal-form-content-close-btn');

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const confirmationCode = document.getElementById('confirmation-code').value;
        const url = `/shift/buscar-turno/?confirmation_code=${encodeURIComponent(confirmationCode)}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json()) 
        .then(data => {
            openModal(data);
        })
        .catch(error => {
            console.error("Error:", error);
            turnoModalBody.innerHTML = `<p>${error.message}</p>`;
            openModal({ error: error.message });
        });
    });

    closeModal.addEventListener('click', function() {
        closeModalFunction();
    });

    turnoModal.addEventListener('click', function(event) {
        if (event.target === turnoModal) {
            closeModalFunction();
        }
    });

    function closeModalFunction() {
        turnoModal.style.display = 'none';
        document.getElementById('confirmation-code').value = '';
    }

    function openModal(data) {
        turnoModal.style.display = 'flex';
        if (data.error) {
            turnoModalBody.innerHTML = `<p>${data.error}</p>`;
        } else {
            const turnoDetalle = data.turno_detalle;
            turnoModalBody.innerHTML = `
                <p><strong>Fecha:</strong> ${turnoDetalle.date}</p>
                <p><strong>Hora:</strong> ${turnoDetalle.hour}</p>
                <p><strong>Nombre:</strong> ${turnoDetalle.first_name} ${turnoDetalle.last_name}</p>
                <p><strong>Email:</strong> ${turnoDetalle.email}</p>
            `;
        }
    }
});

