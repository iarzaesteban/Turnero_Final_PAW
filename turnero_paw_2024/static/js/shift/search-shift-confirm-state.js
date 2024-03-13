document.addEventListener('DOMContentLoaded', function() {
    const shiftsContainer = document.getElementById('shifts-confirm-state-container');
    const turnosHoyButton = document.getElementById('get-shift-confirm-state-btn');
    let isShiftsContainerVisible = true;

    turnosHoyButton.addEventListener('click', function() {
        isShiftsContainerVisible = !isShiftsContainerVisible;
        if (isShiftsContainerVisible) {
            console.log("sadsadasd", isShiftsContainerVisible);
            shiftsContainer.style.display = 'none';
            turnosHoyButton.innerText = 'Turnos Para Hoy';
        }else{
            getShiftsConfirmState();
            shiftsContainer.style.display = 'block';
            turnosHoyButton.innerText = 'Cerrar';
        }
        turnosHoyButton.style.display = 'block';     
    });

    function getShiftsConfirmState(){
        fetch('/shift/get-shifts-today/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            shiftsContainer.innerHTML = '';

            if (data.shifts_today.length > 0) {
                data.shifts_today.forEach(shift => {
                    const shiftHtml = `
                        <span id="shifts-container__list-shifts">
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
                shiftsContainer.innerHTML = '<li>No hay turnos confirmados para hoy.</li>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

//     turnosHoyButton.addEventListener('click', function() {
//         console.log("isShiftsContainerVisible", isShiftsContainerVisible);
//         if (isShiftsContainerVisible) {
//             console.log("sadsadasd", isShiftsContainerVisible);
//             shiftsContainer.style.display = 'none';
//             turnosHoyButton.innerText = 'Turnos Para Hoy';
//         } else {
//             fetch('/shift/get-shifts-today/', {
//                 method: 'GET',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 }
//             })
//             .then(response => response.json())
//             .then(data => {
//                 shiftsContainer.innerHTML = '';

//                 if (data.shifts_today.length > 0) {
//                     data.shifts_today.forEach(shift => {
//                         const shiftHtml = `
//                             <section id="shifts-container__list-shifts">
//                                 <p>
//                                     <strong>Solicitado por:</strong> ${shift.id_person}
//                                 </p>
//                                 <p>
//                                     <strong>Fecha:</strong> ${shift.date}
//                                 </p>
//                                 <p>
//                                     <strong>Hora:</strong> ${shift.hour}
//                                 </p>
//                                 <p>
//                                     <strong>Email:</strong> ${shift.mail}
//                                 </p>
//                             </section>
//                         `;
//                         shiftsContainer.insertAdjacentHTML('beforeend', shiftHtml);
//                     });
//                 } else {
//                     shiftsContainer.innerHTML = '<li>No hay turnos confirmados para hoy.</li>';
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });

//             
//             turnosHoyButton.innerText = 'Cerrar';
//         }
//         isShiftsContainerVisible = !isShiftsContainerVisible;
//         console.log("isShiftsContainerVisible", isShiftsContainerVisible);
//     });
// });
