document.addEventListener('DOMContentLoaded', function() {
    const shiftsContainerConfirm = document.getElementById('shifts-data-states-container');
    const shiftsPendingStateBtn = document.getElementById('get-shift-pending-state-btn');
    const shiftsConfirmStateBtn = document.getElementById('get-shift-confirm-state-btn');
    let isShiftsContainerPendingVisible = true;
    let isShiftsContainerConfirmVisible = true;

    shiftsConfirmStateBtn.addEventListener('click', function() {
        if(!isShiftsContainerPendingVisible){
            shiftsPendingStateBtn.innerText = 'Turnos Pendientes Para Hoy';
            isShiftsContainerPendingVisible = true;
        }
        isShiftsContainerConfirmVisible = !isShiftsContainerConfirmVisible;
        if (isShiftsContainerConfirmVisible) {
            shiftsContainerConfirm.style.display = 'none';
            shiftsConfirmStateBtn.innerText = 'Turnos Confirmados Para Hoy';
        } else {
            getShiftsState('confirmado', shiftsContainerConfirm, shiftsConfirmStateBtn);            
        }
    });

    shiftsPendingStateBtn.addEventListener('click', function() {
        if(!isShiftsContainerConfirmVisible){
            shiftsConfirmStateBtn.innerText = 'Turnos Confirmados Para Hoy';
            isShiftsContainerConfirmVisible = true;
        }
        isShiftsContainerPendingVisible = !isShiftsContainerPendingVisible;
        if (isShiftsContainerPendingVisible) {
            shiftsContainerConfirm.style.display = 'none';
            shiftsPendingStateBtn.innerText = 'Turnos Pendientes Para Hoy';
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
                data.shifts_today.forEach(shift => {
                    const shiftHtml = `
                        <span id="shifts-container__list-shifts">
                            <h3> Turnos ${state} para hoy </h3>
                            <p>
                                <strong>Solicitado por:</strong> ${shift.id_person}
                            </p>
                            <p>
                                <strong>Fecha:</strong> ${shift.date}
                            </p>
                            <p>
                                <strong>Hora:</strong> ${shift.hour}
                            </p>
                            <p>
                                <strong>Email:</strong> ${shift.mail}
                            </p>
                        </span>
                    `;
                    shiftsContainer.insertAdjacentHTML('beforeend', shiftHtml);
                });
            } else {
                shiftsContainer.innerHTML = `<h3> No hay turnos ${state} para hoy </h3>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        shiftsContainer.style.display = 'block';
        shiftsContainer.style.border = 'red 5px solid';
        button.innerText = 'Cerrar';
    }
});
