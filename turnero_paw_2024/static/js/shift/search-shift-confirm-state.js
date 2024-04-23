document.addEventListener('DOMContentLoaded', function() {
    const getShiftsBtns = document.querySelectorAll('.get-shifts-btn');

    getShiftsBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     const shiftsContainerConfirm = document.getElementById('shifts-data-states-container');
//     const shiftsPendingStateBtn = document.getElementById('get-shift-pending-state-btn');
//     const shiftsConfirmStateBtn = document.getElementById('get-shift-confirm-state-btn');
//     const footerCardsContainer = document.getElementById('footer-cards-container');
//     let isShiftsContainerPendingVisible = true;
//     let isShiftsContainerConfirmVisible = true;

//     const paginationContainer = document.querySelector('.pagination-container');

//     if (paginationContainer){
//         paginationContainer.classList.add("pagination-for-reports")
//     }
    

//     function createPagination(data) {
//         console.log()
//         paginationContainer.innerHTML = '';
//         const stepLinks = document.createElement('span');
//         stepLinks.classList.add('step-links');
//         if (data.page_obj) {
//             if (data.page_obj.has_previous) {
//                 const firstLink = document.createElement('a');
//                 firstLink.href = `?page=1`;
//                 firstLink.innerText = '1';
//                 firstLink.setAttribute('data-page', 1);
//                 stepLinks.appendChild(firstLink);
    
//                 const prevLink = document.createElement('a');
//                 prevLink.href = `?page=${data.page_obj.previous_page_number}`;
//                 prevLink.innerText = ' < ';
//                 prevLink.setAttribute('data-page', data.page_obj.previous_page_number);
//                 stepLinks.appendChild(prevLink);
//             }
    
//             const currentSpan = document.createElement('span');
//             currentSpan.classList.add('current');
//             currentSpan.innerText = `Página ${data.page_obj.number} de ${data.page_obj.paginator}`;
//             stepLinks.appendChild(currentSpan);
    
//             if (data.page_obj.has_next) {
//                 const nextLink = document.createElement('a');
//                 nextLink.href = `?page=${data.page_obj.next_page_number}`;
//                 nextLink.innerText = ' > ';
//                 nextLink.setAttribute('data-page', data.page_obj.next_page_number);
//                 stepLinks.appendChild(nextLink);
    
//                 const lastLink = document.createElement('a');
//                 lastLink.href = `?page=${data.page_obj.paginator}`;
//                 lastLink.innerText = data.page_obj.paginator;
//                 lastLink.setAttribute('data-page', data.page_obj.paginator);
//                 stepLinks.appendChild(lastLink);
//             }
//         }
    
//         paginationContainer.appendChild(stepLinks);
//     }

//     shiftsConfirmStateBtn.addEventListener('click', function() {
//         if(!isShiftsContainerPendingVisible){
//             shiftsPendingStateBtn.innerText = 'Turnos Pendientes Hoy';
//             isShiftsContainerPendingVisible = true;
//         }
//         isShiftsContainerConfirmVisible = !isShiftsContainerConfirmVisible;
//         if (isShiftsContainerConfirmVisible) {
//             shiftsContainerConfirm.style.display = 'none';
//             footerCardsContainer.style.bottom = "0";
//             shiftsConfirmStateBtn.innerText = 'Turnos Confirmados Hoy';
//         } else {
//             getShiftsState('confirmado', shiftsContainerConfirm, shiftsConfirmStateBtn);            
//         }
//     });

//     shiftsPendingStateBtn.addEventListener('click', function() {
//         if(!isShiftsContainerConfirmVisible){
//             shiftsConfirmStateBtn.innerText = 'Turnos Confirmados Hoy';
//             isShiftsContainerConfirmVisible = true;
//         }
//         isShiftsContainerPendingVisible = !isShiftsContainerPendingVisible;
//         if (isShiftsContainerPendingVisible) {
//             shiftsContainerConfirm.style.display = 'none';
//             footerCardsContainer.style.bottom = "0";
//             shiftsPendingStateBtn.innerText = 'Turnos Pendientes Hoy';
//         } else {
//             getShiftsState('pendiente', shiftsContainerConfirm, shiftsPendingStateBtn);
//         }
//     });

//     function getShiftsState(state, shiftsContainer, button) {
//         fetch(`/shift/get-shifts-today/?state=${state}`, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log("DATA ES ",data)
//             console.log("DATA ES ",data.serialized_data)
//             shiftsContainer.innerHTML = '';
//             if (data.serialized_data.length > 0) {
//                 const titleShitsHtml = `<h3> Turnos ${state}s para hoy </h3>`;
//                 shiftsContainer.insertAdjacentHTML('beforeend', titleShitsHtml);
//                 data.serialized_data.forEach(shift => {
//                     const shiftDate = new Date(shift.date);
//                     const formattedDate = `${shiftDate.getDate() + 1 } de ${getMonthName(shiftDate.getMonth())} de ${shiftDate.getFullYear()}`;
//                     const formattedHour = shift.hour.slice(0, 5);
//                     const shiftHtml = `
//                         <section id="shifts-container-section__fetch">
//                             <p>
//                                 <strong>Solicitado por:</strong> ${shift.id_person}
//                             </p>
//                             <p>
//                                 <strong>Fecha:</strong> ${formattedDate}
//                             </p>
//                             <p>
//                                 <strong>Hora:</strong> ${formattedHour}
//                             </p>
//                             <p>
//                                 <strong>Email:</strong> ${shift.mail}
//                             </p>
//                         </span>
//                     `;
//                     shiftsContainer.insertAdjacentHTML('beforeend', shiftHtml);
//                 });
//             } else {
//                 shiftsContainer.innerHTML = `<h3> No hay turnos ${state}s para hoy </h3>`;
                
//                 shiftsContainer.style.border = '.1rem solid #ccc';
//                 shiftsContainer.style.borderRadius = '.5rem';
//                 shiftsContainer.style.boxShadow = '0 0 1rem rgba(0, 0, 0, 0.1)';
//                 shiftsContainer.style.margin = '5rem .5rem';
//                 shiftsContainer.style.padding = '1rem';
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//         createPagination(data);
//         correctPositionFooter();
//         shiftsContainer.style.display = 'flex';
//         button.innerText = 'Cerrar';
//     }

//     function correctPositionFooter(){
//         const footerRect = footerCardsContainer.getBoundingClientRect();
//         const windowHeight = window.innerHeight;
//         const spaceBelowFooter = windowHeight - footerRect.bottom;
//         if(spaceBelowFooter > -1){
//             footerCardsContainer.style.removeProperty("bottom");
//         }
//     }

//     function getMonthName(monthNumber) {
//         const months = ["Enero", "Febrero", "Marzo", 
//                         "Abril", "Mayo", "Junio", 
//                         "Julio", "Agosto", "Septiembre", "Octubre", 
//                         "Noviembre", "Diciembre"];
//         return months[monthNumber];
//     }
    
// });