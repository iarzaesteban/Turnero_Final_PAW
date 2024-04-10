import {
    currentYear,
    currentMonth,
    currentDay,
} from './index.js';

const emailInput = document.getElementById("emailInput");
const lastNameInput = document.getElementById("apellidoInput");
const nameInput = document.getElementById("nombreInput");
const requestShiftBtn = document.getElementById("modal-form-content-request-shift-btn");
const modalErrorText = document.getElementById('modal-email-error-text');
const modalContent = document.getElementById('modal-content');
const timeParagraph = document.getElementById('selectedTime');
const dateParagraph = document.getElementById('selectedDate');
const calendarContainer = document.getElementById('calendar-container');
let hourShift = "";
let minutesShift = "";

export function openModal(formattedHour, formattedMinute, 
                            dayOfWeek, stringMonth, currentYear) {
    const modal = document.getElementById('appointmentModal');
    const shiftTime = `${formattedHour}:${formattedMinute}hs`;
    const shiftDate =  `${dayOfWeek} ${currentDay} de ${stringMonth} 
                                            de ${currentYear}`
    hourShift =  formattedHour;
    minutesShift =  formattedMinute;                                   
    timeParagraph.textContent = shiftTime;
    dateParagraph.textContent = shiftDate;
    modal.style.display = 'flex';
}

export function closeModal() {
    const errorMessageParagraph = document.getElementById('modal-error-message');
    errorMessageParagraph.style.display = "none";
    emailInput.value = "";
    lastNameInput.value = "";
    nameInput.value = "";
    const modal = document.getElementById('appointmentModal');
    modal.style.display = 'none';
    emailInput.classList.remove('input-error');
    modalErrorText.classList.remove('modal-email-error-text-show');
    modalContent.style.height = '';
    requestShiftBtn.disabled = true;
}

document.addEventListener('DOMContentLoaded', function() {
    const closeButton = document.getElementById('modal-form-content-close-btn');
    if (closeButton) {
        closeButton.addEventListener('click', closeModal);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const requestShiftButton = document.getElementById('modal-form-content-request-shift-btn');
    if (requestShiftButton) {
        requestShiftButton.addEventListener('click', requestShift);
    }else{
        
    }
});

function formattedDate(selectedDate){
    const year = selectedDate.getFullYear();
    const month = String(selectedDate.getMonth() + 1).padStart(2, '0');
    const day = String(selectedDate.getDate()).padStart(2, '0');
    const hours = String(selectedDate.getHours()).padStart(2, '0');
    const minutes = String(selectedDate.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}`
}

export function requestShift() {
    if (validateEmailFormat(emailInput.value.trim())){
        const selectedDate = new Date(currentYear, currentMonth, currentDay, hourShift, minutesShift);
        console.log("selectedDate", selectedDate);

        const formatDate = formattedDate(selectedDate);
        console.log("formattedDate", formatDate);
        fetch('/shift/confirm_shift/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                email: emailInput.value,
                dateTime: formatDate,
                name: nameInput.value,
                last_name: lastNameInput.value
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al solicitar turno');
            }
            return response.json();
        })
        .then(data => {
            if (data.shift){
                const message = `Se ha solicitado un turno para ${data.shift.person} el día ${data.shift.day}, a las ${data.shift.hour}. El turno será evaluado por un operador y se le notificará a su casilla de mail.`;
                const messageRequestShift = document.createElement('p');
                messageRequestShift.textContent = message;
                const firstChild = calendarContainer.firstChild;
                calendarContainer.insertBefore(messageRequestShift, firstChild);
                closeModal()
                setTimeout(function() {
                    calendarContainer.removeChild(messageRequestShift);
                }, 5000);
            } else if (data.response == "error"){
                showErrorMessage(data.message);
            }
        })
        .catch(error => {
            console.error('Error al solicitar turno:', error);
            showErrorMessage('Error al solicitar turno');
        });
    } else {
        emailInput.classList.add('input-error');
        showErrorMessage('El correo electrónico ingresado es inválido');
    }
}

function showSuccessMessage(message) {
    const messageParagraph = document.getElementById('modal-error-message');
    messageParagraph.textContent = message;
    emailInput.value = "";
    lastNameInput.value = "";
    nameInput.value = "";
    messageParagraph.classList.add('modal-message-show');
    messageParagraph.style.display = 'block';
    modalContent.style.height = '43rem';
    requestShiftBtn.disabled = true;
}

function showErrorMessage(errorMessage) {
    const errorMessageParagraph = document.getElementById('modal-error-message');
    errorMessageParagraph.textContent = errorMessage;
    errorMessageParagraph.classList.add('modal-error-message-show');
    errorMessageParagraph.style.display = 'block';
    errorMessageParagraph.style.color = 'red';
    modalContent.style.height = '40rem';
    requestShiftBtn.disabled = true;
}

function validateEmailFormat(email) {
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regexEmail.test(email);
}

function validarCampos() {
    const email = emailInput.value.trim();
    const apellido = lastNameInput.value.trim();
    const nombre = nameInput.value.trim();
    requestShiftBtn.disabled = !(email && apellido && nombre);
}

document.addEventListener("DOMContentLoaded", function() {
    emailInput.addEventListener("input", validarCampos);
    lastNameInput.addEventListener("input", validarCampos);
    nameInput.addEventListener("input", validarCampos);

    
});
