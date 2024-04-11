document.addEventListener('DOMContentLoaded', function() {
    const shiftsContainerConfirm = document.getElementById('shifts-data-states-container');
    const shiftsPendingStateBtn = document.getElementById('get-shift-pending-state-btn');
    const shiftsConfirmStateBtn = document.getElementById('get-shift-confirm-state-btn');
    let isShiftsContainerPendingVisible = true;
    let isShiftsContainerConfirmVisible = true;

    shiftsConfirmStateBtn.addEventListener('click', function() {
        if(!isShiftsContainerPendingVisible){
            shiftsPendingStateBtn.innerText = 'Turnos Pendientes Hoy';
            isShiftsContainerPendingVisible = true;
        }
        isShiftsContainerConfirmVisible = !isShiftsContainerConfirmVisible;
        if (isShiftsContainerConfirmVisible) {
            shiftsContainerConfirm.style.display = 'none';
            shiftsConfirmStateBtn.innerText = 'Turnos Confirmados Hoy';
        } else {
            getShiftsState('confirmado', shiftsContainerConfirm, shiftsConfirmStateBtn);            
        }
    });

    shiftsPendingStateBtn.addEventListener('click', function() {
        if(!isShiftsContainerConfirmVisible){
            shiftsConfirmStateBtn.innerText = 'Turnos Confirmados Hoy';
            isShiftsContainerConfirmVisible = true;
        }
        isShiftsContainerPendingVisible = !isShiftsContainerPendingVisible;
        if (isShiftsContainerPendingVisible) {
            shiftsContainerConfirm.style.display = 'none';
            shiftsPendingStateBtn.innerText = 'Turnos Pendientes Hoy';
        } else {
            getShiftsState('pendiente', shiftsContainerConfirm, shiftsPendingStateBtn);
        }
    });

    function getShiftsState(state, shiftsContainer, button) {
        fetch(`/shift/get-shifts-today/?state=${state}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("DATA ES ",data)
            shiftsContainer.innerHTML = '';
            if (data.shifts_today.length > 0) {
                const titleShitsHtml = `<h3> Turnos ${state}s para hoy </h3>`;
                shiftsContainer.insertAdjacentHTML('beforeend', titleShitsHtml);
                data.shifts_today.forEach(shift => {
                    const shiftDate = new Date(shift.date);
                    const formattedDate = `${shiftDate.getDate() + 1 } de ${getMonthName(shiftDate.getMonth())} de ${shiftDate.getFullYear()}`;
                    const formattedHour = shift.hour.slice(0, 5);
                    const shiftHtml = `
                        <section id="shifts-container-section__fetch">
                            <p>
                                <strong>Solicitado por:</strong> ${shift.id_person}
                            </p>
                            <p>
                                <strong>Fecha:</strong> ${formattedDate}
                            </p>
                            <p>
                                <strong>Hora:</strong> ${formattedHour}
                            </p>
                            <p>
                                <strong>Email:</strong> ${shift.mail}
                            </p>
                        </span>
                    `;
                    shiftsContainer.insertAdjacentHTML('beforeend', shiftHtml);
                });
            } else {
                shiftsContainer.innerHTML = `<h3> No hay turnos ${state}s para hoy </h3>`;
                
                shiftsContainer.style.border = '.1rem solid #ccc';
                shiftsContainer.style.borderRadius = '.5rem';
                shiftsContainer.style.boxShadow = '0 0 1rem rgba(0, 0, 0, 0.1)';
                shiftsContainer.style.margin = '5rem .5rem';
                shiftsContainer.style.padding = '1rem';
                }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        shiftsContainer.style.display = 'flex';
        button.innerText = 'Cerrar';
    }

    function getMonthName(monthNumber) {
        const months = ["Enero", "Febrero", "Marzo", 
                        "Abril", "Mayo", "Junio", 
                        "Julio", "Agosto", "Septiembre", "Octubre", 
                        "Noviembre", "Diciembre"];
        return months[monthNumber];
    }
    
});