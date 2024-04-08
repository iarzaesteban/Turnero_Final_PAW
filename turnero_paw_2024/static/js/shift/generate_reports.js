document.addEventListener('DOMContentLoaded', function() {
    const queryNumber = JSON.parse(document.getElementById('queryNumber').textContent);
    let formData = new FormData();
    const filterForm = document.getElementById('filter-form');
    const shiftsTable = document.getElementById('shifts-table');
    const tHead = document.getElementById('shifts-table__thead');
    const tBody = document.getElementById('shifts-table__tbody');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const stateInput = document.getElementById('state');
    const paginationContainer = document.querySelector('.pagination-container');
    var isFilter = false;
    function createPagination(data) {
        paginationContainer.innerHTML = '';
        const stepLinks = document.createElement('span');
        stepLinks.classList.add('step-links');
        if (data.page_obj) {
            if (data.page_obj.has_previous) {
                const firstLink = document.createElement('a');
                firstLink.href = `?page=1&query=${data.query_number}`;
                firstLink.innerText = 'Primera';
                firstLink.setAttribute('data-page', 1);
                stepLinks.appendChild(firstLink);
    
                const prevLink = document.createElement('a');
                prevLink.href = `?page=${data.page_obj.previous_page_number}&query=${data.query_number}`;
                prevLink.innerText = '‹ Anterior';
                prevLink.setAttribute('data-page', data.page_obj.previous_page_number);
                stepLinks.appendChild(prevLink);
            }
    
            const currentSpan = document.createElement('span');
            currentSpan.classList.add('current');
            currentSpan.innerText = `Página ${data.page_obj.number} de ${data.page_obj.paginator}`;
            stepLinks.appendChild(currentSpan);
    
            if (data.page_obj.has_next) {
                const nextLink = document.createElement('a');
                nextLink.href = `?page=${data.page_obj.next_page_number}&query=${data.query_number}`;
                nextLink.innerText = 'Siguiente ›';
                nextLink.setAttribute('data-page', data.page_obj.next_page_number);
                stepLinks.appendChild(nextLink);
    
                const lastLink = document.createElement('a');
                lastLink.href = `?page=${data.page_obj.paginator}&query=${data.query_number}`;
                lastLink.innerText = 'Última';
                lastLink.setAttribute('data-page', data.page_obj.paginator);
                stepLinks.appendChild(lastLink);
            }
        }
    
        paginationContainer.appendChild(stepLinks);
    }

    function fetchPage(pageNumber) {
        console.log("fetchPage ", pageNumber)
        formData.append('page', pageNumber);

        fetch('/list-shifts-filter-views/', {
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
        
            data.serialized_data.forEach(shift => {
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
            createPagination(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    paginationContainer.addEventListener('click', function(event) {
        if (event.target.tagName === 'A' && isFilter) {
            event.preventDefault();
            console.log("adentro del if")
            const pageNumber = event.target.getAttribute('data-page');
            console.log("pageNumber", pageNumber)
            fetchPage(pageNumber);
        }
    });

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

        formData = new FormData(filterForm);
        formData.append('query', queryNumber); 
        isFilter = true;
        fetchPage(1);
    });

    function exportarExcel() {
        const tableData = [];
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        const rows = document.querySelectorAll('#shifts-table tbody tr');
        if (rows.length === 0) {
            alert('La tabla no tiene datos para exportar.');
            return;
        }
        
        const headerRow = [];
        document.querySelectorAll('#shifts-table thead th').forEach(header => {
            headerRow.push(header.textContent);
        });
        tableData.push(headerRow);

        rows.forEach(row => {
            const rowData = [];
            const cells = row.querySelectorAll('td');
            cells.forEach(cell => {
                rowData.push(cell.textContent);
            });
            tableData.push(rowData);
        });

        fetch('/export-to-excel/', {
            method: 'GET',
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