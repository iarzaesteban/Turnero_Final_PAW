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
    if (validarFormatoEmail(emailInput.value.trim())){
        const selectedDate = new Date(currentYear, currentMonth, currentDay, hourShift, minutesShift);
        console.log("selectedDate", selectedDate);

        const formatDate = formattedDate(selectedDate);
        console.log("formattedDate", formatDate);
        fetch('/shift/confirm_shift/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            
            body: JSON.stringify({ email: emailInput.value,
                                    dateTime: formatDate,
                                    name: nameInput.value,
                                    last_name: lastNameInput.value}),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.events);  
        })
        .catch(error => {
            console.error('Error fetching Google Calendar events:', error);
        });
    }else{
        emailInput.classList.add('input-error');
        showErrorMessage();
    }
}

function showErrorMessage() {
    modalErrorText.classList.add('modal-email-error-text-show');
    modalContent.style.height = '40rem';
}

function validarFormatoEmail(email) {
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
