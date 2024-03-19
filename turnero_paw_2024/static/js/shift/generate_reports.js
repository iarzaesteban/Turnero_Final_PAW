document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    const shiftsTable = document.getElementById('shifts-table');

    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const stateInput = document.getElementById('state');


    filterForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        if (!startDateInput.value && !endDateInput.value && !stateInput.value) {
            alert("Por favor seleccione al menos una opción para filtrar.");
            return;
        }
        if (!startDateInput.value && endDateInput.value) {
            alert("Por favor seleccione una Fecha Desde.");
            return;
        } else if (startDateInput.value && !endDateInput.value) {
            alert("Por favor seleccione una Fecha Hasta.");
            return;
        }

        const formData = new FormData(filterForm);
        const url = filterForm.dataset.reportsUrl;

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            shiftsTable.innerHTML = '';
        
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = `
                <th>Fecha</th>
                <th>Hora</th>
                <th>Persona</th>
                <th>Operador Asignado</th>
            `;
            shiftsTable.appendChild(headerRow);
        
            data.forEach(shift => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${shift.date}</td>
                    <td>${shift.hour}</td>
                    <td>${shift.id_person}</td>
                    <td>${shift.operador}</td>
                `;
                shiftsTable.appendChild(row);
            });
        
            filterForm.reset();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
