document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    const shiftsTable = document.getElementById('shifts-table');
    const tHead = document.getElementById('shifts-table__thead');
    const tBody = document.getElementById('shifts-table__tbody');

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
            tHead.innerHTML = '';
            tBody.innerHTML = '';
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = `
                <th>Fecha</th>
                <th>Hora</th>
                <th>Persona</th>
                <th>Operador Asignado</th>
            `;
            tHead.appendChild(headerRow);
        
            data.forEach(shift => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${shift.date}</td>
                    <td>${shift.hour}</td>
                    <td>${shift.id_person}</td>
                    <td>${shift.operador}</td>
                `;
                tBody.appendChild(row);
            });
            shiftsTable.appendChild(tHead);
            shiftsTable.appendChild(tBody);
            filterForm.reset();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function exportarExcel() {
        console.log("precionado")
        const tableData = [];
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        const headerRow = [];
        document.querySelectorAll('#shifts-table thead th').forEach(header => {
            console.log("LOS HEADERS SON", header)
            headerRow.push(header.textContent);
        });
        tableData.push(headerRow);

        const rows = document.querySelectorAll('#shifts-table tbody tr');
        rows.forEach(row => {
            const rowData = [];
            const cells = row.querySelectorAll('td');
            cells.forEach(cell => {
                rowData.push(cell.textContent);
            });
            tableData.push(rowData);
        });

        fetch('/export-to-excel/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(tableData),
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Error en la respuesta del servidor');
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'reporte_turnos.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    const exportButton = document.querySelector('#export-button');
    exportButton.addEventListener('click', exportarExcel);
    
});
