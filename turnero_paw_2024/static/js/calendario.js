// import {
//     cleanSelectors,
//     updateSelectors
// } from './selectors.js';

let date = new Date();

const thisYear = date.getFullYear();
const thisMonth = date.getMonth();
const lastMonthShow = thisMonth + 2;
const thisDay = date.getDate();

let currentYear = date.getFullYear();
let currentMonth = date.getMonth();
let currentDay = date.getDate();

let firstDayMonth = new Date(currentYear, currentMonth, 1);
let lastDayMonth = new Date(currentYear, currentMonth + 1, 0);

let daysWeek = lastDayMonth.getDate();
let firstDayWeek = firstDayMonth.getDay();

let calendarBody = document.getElementById("calendario-cuerpo");
let monthSelected = document.getElementById("selectMes");
let yearSelected = document.getElementById("selectAnio");

let responseEvents = [];
const startHourWork = 8;
const finishHourWork = 17;
const minutesIterator = 30;

// const eventsData = JSON.parse(
//     document.currentScript.nextElementSibling.textContent
//   );
  
// Generamos/Regeneramos el calendario
function generateCalendar() {
    let day = 1;
    for (let i = 0; i < 6; i++) { 
        const row = calendarBody.insertRow();
    
        for (let j = 0; j < 7; j++) {
            const cell = row.insertCell();
    
            if (i === 0 && j < firstDayWeek) {
                cell.textContent = "";
            } else if (day > daysWeek) {
                cell.textContent = "";
            } else {
                cell.textContent = day;
                cell.classList.add(getClassDay(day));

                if (day >= thisDay || currentMonth != thisMonth ) {
                    cell.addEventListener("click", createClickHandler(day));
                }
                    
                day++;
            }
        }
    }
}

function getClassDay(dia) {
    if (thisMonth === currentMonth) {
        if (dia < currentDay) {
            return "anterior";
        } else if (dia === currentDay) {
            return "actual";
        } else {
            return "posterior";
        }
    } else {
        return "posterior";
    }
}

function setCurrentDay(){
    const currentDateDay = document.getElementById('current-date-day');
    const currentDateDate = document.getElementById('current-date-date');
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    const dayOfWeek = selectedDate.toLocaleDateString
                                        ('es-ES', { weekday: 'long' }).
                                            replace(/^\w/, (c) => c.toUpperCase());

    currentDateDay.textContent = `${currentDay}  ${dayOfWeek}`;
    currentDateDate.textContent = getMonthName(currentMonth) + ` de ${currentYear}`;
}

function generateSchedules() {
    // Eliminamos el select anterior si existe
    const selectedDaySchedule = document.getElementById('selected-day-schedule');
    selectedDaySchedule.innerHTML = '';

    // Ocultamos el párrafo 'info-subtitle'
    const infoSubtitle = document.getElementById('info-subtitle');
    infoSubtitle.style.display = 'none';
    console.log("responseEvents",responseEvents);

    const currentDateDay = document.getElementById('current-date-day');
    const currentDateDate = document.getElementById('current-date-date');
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    const dayOfWeek = selectedDate.toLocaleDateString
                                        ('es-ES', { weekday: 'long' }).
                                            replace(/^\w/, (c) => c.toUpperCase());

    // Creamos nuevos elementos p para cada horario
    for (let hour = startHourWork; hour <= finishHourWork; hour++) {
        for (let minute = 0; minute < 60; minute += minutesIterator) {
            if (hour < finishHourWork || (hour == finishHourWork && minute === 0)) {
                const formattedHour = hour.toString().padStart(2, '0');
                const formattedMinute = minute.toString().padStart(2, '0');
                const formattedTime = `${formattedHour}:${formattedMinute}`;

                const isEventScheduled = responseEvents.some(event => event.formatted_start.includes(formattedTime));

                if (!isEventScheduled) {
                    const scheduleElement = document.createElement('p');
                    scheduleElement.textContent = `${formattedHour}:${formattedMinute}  - Solicitar`;
                    scheduleElement.classList.add('schedule-item');

                    // Agregamos un evento de clic a cada horario
                    scheduleElement.addEventListener('click', () => {
                        openModal(`${formattedHour}:${formattedMinute}hs`, `${dayOfWeek} 
                                        ${currentDay} de ${getMonthName(currentMonth)} 
                                            de ${currentYear}`);
                    });

                    scheduleElement.classList.add('divider-line');

                    // Agregamos el elemento p al contenedor
                    selectedDaySchedule.appendChild(scheduleElement);
                }
            }
        }
    }    

    currentDateDay.textContent = `${currentDay}  ${dayOfWeek}`;
    currentDateDate.textContent = getMonthName(currentMonth) + ` de ${currentYear}`;

    selectedDaySchedule.style.maxHeight = '30rem'; 
    const infoSection = document.getElementById('info-section');
    infoSection.style.display = 'block';
}

function openModal(selectedTime, selectedDate) {
    const modal = document.getElementById('appointmentModal');
    const timeParagraph = document.getElementById('selectedTime');
    const dateParagraph = document.getElementById('selectedDate');
    timeParagraph.textContent = selectedTime;
    dateParagraph.textContent = selectedDate;
    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('appointmentModal');
    modal.style.display = 'none';
}

function createClickHandler(dia) {
    return function() {
        // Eliminamos la clase "selected" a todos los días antes de marcar uno nuevo
        const days = document.querySelectorAll('td');
        days.forEach(d => d.classList.remove('selected'));

        currentDay = dia;
        // Marcamos el día seleccionado
        this.classList.add('selected');
        getGoogleCalendarEvents();
    };
}

function updateAtributesDate(){
    if(currentMonth == thisMonth){
        currentDay = date.getDate();
    }
    firstDayMonth = new Date(currentYear, currentMonth, 1);
    lastDayMonth = new Date(currentYear, currentMonth + 1, 0);
    daysWeek = lastDayMonth.getDate();
    firstDayWeek = firstDayMonth.getDay();
}

function changeMonth(value) {
    const changeMonth = currentMonth + value;
    if (changeMonth == currentMonth){
        currentMonth = monthSelected.selectedIndex;
    }else if (changeMonth < 0 && changeMonth < thisMonth) {
        currentMonth = 11;
        currentYear--;
    } else if (changeMonth > 11 ) {
        currentMonth = 0;
        currentYear++;
    } else if (changeMonth < thisMonth || changeMonth >= lastMonthShow) {
        currentMonth = (changeMonth < thisMonth) ? thisMonth : lastMonthShow;
    } else {
        currentMonth = changeMonth;
    }

    console.log("currentMonth es ", currentMonth);
    calendarBody.innerHTML = "";
    updateAtributesDate();
    generateCalendar();
    updateSelectors();
    monthSelected.selectedIndex = currentMonth;
    yearSelected.selectedIndex = 0;
}

function cleanSelectors(){
    monthSelected.innerHTML = "";
    yearSelected.innerHTML = "";
}

function updateSelectors() {
    // Limpiamos los selectores
    cleanSelectors();
    const option = document.createElement("option");
    option.value = 0;
    monthSelected.add(option);
    // Generamos options para el selector de mes
    for (let i = thisMonth; i < thisMonth + 3; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.text = getMonthName(i);
        monthSelected.add(option);
    }
    // Establecemos el mes actual como seleccionado
    monthSelected.selectedIndex = currentMonth;

    const yearOption = document.createElement("option");
    yearOption.value = 0;
    yearOption.text = currentYear;
    yearSelected.add(yearOption);
    if (thisMonth > 9) {
        const yearOption = document.createElement("option");
        yearOption.value = 1;
        yearOption.text = currentYear + 1;
        yearSelected.add(yearOption);
    }

    // Establecemos el año actual como seleccionado
    yearSelected.selectedIndex = 0;
}

function getMonthName(indice) {
    const meses = ["Enero", "Febrero", "Marzo", 
                    "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", 
                    "Noviembre", "Diciembre"];

    return meses[indice];
}

function getGoogleCalendarEvents() {
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    const formattedDate = selectedDate.toISOString();
    fetch('/get_google_calendar_events/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        
        body: JSON.stringify({ date: formattedDate}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.events);  
        responseEvents = data.events;
        generateSchedules();
    })
    .catch(error => {
        console.error('Error fetching Google Calendar events:', error);
    });
}

generateCalendar();

updateSelectors();

setCurrentDay();