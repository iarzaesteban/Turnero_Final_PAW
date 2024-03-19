document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const shiftDetailModal = document.getElementById('shift-details-modal');
    const turnoModalBody = document.getElementById('shift-details-modal-body');
    const closeModal = document.getElementById('shift-details-modal-content-close-btn');

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const getInputValue = document.getElementById('input-value').value;
        const url = `/shift/search-shift/?search_value=${encodeURIComponent(getInputValue)}`;

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

    shiftDetailModal.addEventListener('click', function(event) {
        if (event.target === shiftDetailModal) {
            closeModalFunction();
        }
    });

    function closeModalFunction() {
        shiftDetailModal.style.display = 'none';
        document.getElementById('input-value').value = '';
    }

    function openModal(data) {
        shiftDetailModal.style.display = 'flex';
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

