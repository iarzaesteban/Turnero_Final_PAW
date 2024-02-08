export function openModal(selectedTime, selectedDate) {
    const modal = document.getElementById('appointmentModal');
    const timeParagraph = document.getElementById('selectedTime');
    const dateParagraph = document.getElementById('selectedDate');
    timeParagraph.textContent = selectedTime;
    dateParagraph.textContent = selectedDate;
    modal.style.display = 'flex';
}

export function closeModal() {
    const modal = document.getElementById('appointmentModal');
    modal.style.display = 'none';
}