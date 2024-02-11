import {
    thisMonth,
    currentYear,
    currentMonth,
    currentDay,
    firstDayMonth,
    lastDayMonth,
    responseEvents,
    calendarBody
} from './index.js';

import {
    generateCalendar
} from './calendar.js';

import {
    updateSelectors
} from './selectors.js';

import {
    openModal
} from './modal.js';

let date = new Date();

const startHourWork = 8;
const finishHourWork = 17;
const minutesIterator = 30;

export function generateSchedules() {
    const selectedDaySchedule = document.getElementById('selected-day-schedule');
    selectedDaySchedule.innerHTML = '';
    
    const infoSubtitle = document.getElementById('info-subtitle');
    infoSubtitle.style.display = 'none';
    console.log("responseEvents",responseEvents);

    const currentDateDay = document.getElementById('current-date-day');
    const currentDateDate = document.getElementById('current-date-date');
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    const dayOfWeek = selectedDate.toLocaleDateString
                                        ('es-ES', { weekday: 'long' }).
                                            replace(/^\w/, (c) => c.toUpperCase());

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

                    scheduleElement.addEventListener('click', () => {
                        openModal(`${formattedHour}:${formattedMinute}hs`, `${dayOfWeek} 
                                        ${currentDay} de ${getMonthName(currentMonth)} 
                                            de ${currentYear}`);
                    });

                    scheduleElement.classList.add('divider-line');
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

export function getClassDay(day) {
    if (thisMonth === currentMonth) {
        if (day < currentDay) {
            return "anterior";
        } else if (day === currentDay) {
            return "actual";
        } else {
            return "posterior";
        }
    } else {
        return "posterior";
    } 
}

export function updateAtributesDate(){
    if(currentMonth == thisMonth){
        currentDay = date.getDate();
    }
    
    firstDayMonth = new Date(currentYear, currentMonth, 1);
    lastDayMonth = new Date(currentYear, currentMonth + 1, 0);
    daysWeek = lastDayMonth.getDate();
    firstDayWeek = firstDayMonth.getDay();
}

export function setCurrentDate(){
    const currentDateDay = document.getElementById('current-date-day');
    const currentDateDate = document.getElementById('current-date-date');
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    const dayOfWeek = selectedDate.toLocaleDateString
                                        ('es-ES', { weekday: 'long' }).
                                            replace(/^\w/, (c) => c.toUpperCase());
    currentDateDay.textContent = `${currentDay}  ${dayOfWeek}`;
    currentDateDate.textContent = getMonthName(currentMonth) + ` de ${currentYear}`;
}

export function getMonthName(indice) {
    const meses = ["Enero", "Febrero", "Marzo", 
                    "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", 
                    "Noviembre", "Diciembre"];

    return meses[indice];
}



export function changeMonth(value) {
    const thisMonth = date.getMonth();
    currentDay = date.getDate();
    const lastMonthShow = thisMonth + 2;

    let monthSelected = document.getElementById("selectMonth");
    let yearSelected = document.getElementById("selectYear");
    const changeMonth = monthSelected.selectedIndex + value;
    const changeYear = yearSelected.selectedIndex;
    if (changeMonth == currentMonth){
        currentMonth = monthSelected.selectedIndex;
    }else if (changeMonth < 0 && changeMonth < thisMonth) {
        changeMonth = 11;
        changeYear--;
    } else if (changeMonth > 11 ) {
        changeMonth = 0;
        changeYear++;
    } else if (changeMonth < thisMonth || changeMonth >= lastMonthShow) {
        changeMonth = (changeMonth < thisMonth) ? thisMonth : lastMonthShow;
    }

    console.log("changeMonth es ", changeMonth);
    calendarBody.innerHTML = "";
    updateAtributesDate();
    generateCalendar();
    updateSelectors();
    monthSelected.selectedIndex = changeMonth;
    yearSelected.selectedIndex = 0;
}