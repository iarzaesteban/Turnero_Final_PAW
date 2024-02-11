const emailInput = document.getElementById("emailInput");
const apellidoInput = document.getElementById("apellidoInput");
const nombreInput = document.getElementById("nombreInput");
const solicitarTurnoBtn = document.getElementById("modal-form-content-request-shift-btn");
const modalErrorText = document.getElementById('modal-email-error-text');
const modalContent = document.getElementById('modal-content');

export function openModal(selectedTime, selectedDate) {
    const modal = document.getElementById('appointmentModal');
    const timeParagraph = document.getElementById('selectedTime');
    const dateParagraph = document.getElementById('selectedDate');
    timeParagraph.textContent = selectedTime;
    dateParagraph.textContent = selectedDate;
    modal.style.display = 'flex';
}

export function closeModal() {
    emailInput.value = "";
    apellidoInput.value = "";
    nombreInput.value = "";
    const modal = document.getElementById('appointmentModal');
    modal.style.display = 'none';
    emailInput.classList.remove('input-error');
    modalErrorText.classList.remove('modal-email-error-text-show');
    modalContent.style.height = '';
    solicitarTurnoBtn.disabled = true;
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

export function requestShift() {
    if (validarFormatoEmail(emailInput.value.trim())){
        alert("por solicitar el turno")
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
    const apellido = apellidoInput.value.trim();
    const nombre = nombreInput.value.trim();
    solicitarTurnoBtn.disabled = !(email && apellido && nombre);
}

document.addEventListener("DOMContentLoaded", function() {
    emailInput.addEventListener("input", validarCampos);
    apellidoInput.addEventListener("input", validarCampos);
    nombreInput.addEventListener("input", validarCampos);

    
});
