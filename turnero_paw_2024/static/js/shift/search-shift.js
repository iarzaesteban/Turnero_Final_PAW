document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-shift-section__form');
    const shiftDetailModal = document.getElementById('shift-details-modal');
    const turnoModalBody = document.getElementById('shift-details-modal-body');
    const closeModal = document.getElementById('close-modal-btn');

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const getInputValue = document.getElementById('search-shift-section__input').value;
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
        document.getElementById('search-shift-section__input').value = '';
    }

    function openModal(data) {
        shiftDetailModal.style.display = 'flex';
        if (data.error) {
            turnoModalBody.innerHTML = `<p>${data.error}</p>`;
        } else {
            const turnoDetalle = data.turno_detalle;
            console.log("turnodetalle es", turnoDetalle)
            const shiftDate = new Date(turnoDetalle.date);
            const formattedDate = `${shiftDate.getDate() + 1} de ${getMonthName(shiftDate.getMonth())} de ${shiftDate.getFullYear()}`;
            const formattedHour = turnoDetalle.hour.slice(0, 5);
            turnoModalBody.innerHTML = `
                <p><strong>Fecha:</strong> ${formattedDate}</p>
                <p><strong>Hora:</strong> ${formattedHour}</p>
                <p><strong>Estado:</strong> ${turnoDetalle.state}</p>
                <p><strong>Nombre:</strong> ${turnoDetalle.first_name} ${turnoDetalle.last_name}</p>
                <p><strong>Email:</strong> ${turnoDetalle.email}</p>
            `;
        }
    }

    function getMonthName(monthNumber) {
        const months = ["Enero", "Febrero", "Marzo", 
                        "Abril", "Mayo", "Junio", 
                        "Julio", "Agosto", "Septiembre", "Octubre", 
                        "Noviembre", "Diciembre"];
        return months[monthNumber];
    }
});

