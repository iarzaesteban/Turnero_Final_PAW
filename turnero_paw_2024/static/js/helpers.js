import {
    thisMonth,
    currentYear,
    currentMonth,
    currentDay,
    setCurrentDay,
    firstDayMonth,
    setFirstDayMonth,
    lastDayMonth,
    setlastDayMonth,
    lastMonthShow,
    setDaysWeek,
    setnFirstDayWeek,
    responseEvents,
    startTimeAttention,
    endTimeAttention,
    setCurrentMonth,
    setCurrentYear,
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

let monthSelected = document.getElementById("selectMonth");
let yearSelected = document.getElementById("selectYear");

export function generateSchedules() {
    const selectedDaySchedule = document.getElementById('selected-day-schedule');
    selectedDaySchedule.innerHTML = '';

    const infoSubtitle = document.getElementById('info-subtitle');
    infoSubtitle.style.display = 'none';

    const currentDateDay = document.getElementById('current-date-day');
    const currentDateDate = document.getElementById('current-date-date');
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    const dayOfWeek = selectedDate.toLocaleDateString
                                        ('es-ES', { weekday: 'long' }).
                                            replace(/^\w/, (c) => c.toUpperCase());

    const startTime = new Date(`2000-01-01T${startTimeAttention}:00`);
    const endTime = new Date(`2000-01-01T${endTimeAttention}:00`);
    let currentTime = startTime;

    while (currentTime <= endTime) {
        const hour = currentTime.getHours();
        const minute = currentTime.getMinutes();
        const formattedHour = hour.toString().padStart(2, '0');
        const formattedMinute = minute.toString().padStart(2, '0');
        const formattedTime = `${formattedHour}:${formattedMinute}`;
        const isEventScheduled = responseEvents.some(event => event.formatted_start.includes(formattedTime));

        if (!isEventScheduled) {
            const scheduleElement = document.createElement('p');
            scheduleElement.textContent = `${formattedHour}:${formattedMinute} - Solicitar`;
            scheduleElement.classList.add('schedule-item');
        
            scheduleElement.addEventListener('click', () => {
                openModal(formattedHour, formattedMinute, 
                                dayOfWeek, 
                                getMonthName(currentMonth), currentYear);
            });
            scheduleElement.classList.add('divider-line');
        
            selectedDaySchedule.appendChild(scheduleElement);
        }
    
        currentTime.setMinutes(currentTime.getMinutes() + 30);
    }

    currentDateDay.textContent = `${currentDay}  ${dayOfWeek}`;
    currentDateDate.textContent = getMonthName(currentMonth) + ` de ${currentYear}`;

    const windowWidth = getWindowWidth();
    if (windowWidth >= 768 ) {
        selectedDaySchedule.style.maxHeight = '24rem';
    } 
    selectedDaySchedule.style.marginTop = '1rem';
    const infoSection = document.getElementById('info-section');
    infoSection.style.display = 'flex';
    infoSection.style.gap = "0";
}

function getWindowWidth() {
    return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
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
        setCurrentDay(date.getDate());
    }
    
    setFirstDayMonth(new Date(currentYear, currentMonth, 1));
    setlastDayMonth(new Date(currentYear, currentMonth + 1, 0));
    setDaysWeek(lastDayMonth.getDate());
    setnFirstDayWeek(firstDayMonth.getDay());
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

export function getMonthName(monthNumber) {
    const months = ["Enero", "Febrero", "Marzo", 
                    "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", 
                    "Noviembre", "Diciembre"];
    return months[monthNumber];
}

export function changeMonth(value) {
    
    const changeMonth = currentMonth + value;
    
    if (changeMonth == currentMonth){
        setCurrentMonth(monthSelected.selectedIndex);
    }else if (changeMonth < 0 && changeMonth < thisMonth) {
        setCurrentMonth(11);
        currentYear--;
    } else if (changeMonth > 11 ) {
        setCurrentMonth(0);
        currentYear++;
    } else if (changeMonth < thisMonth || changeMonth >= lastMonthShow) {
        setCurrentMonth((changeMonth < thisMonth) ? thisMonth : lastMonthShow);
    } else {
        setCurrentMonth(changeMonth);
    }

    calendarBody.innerHTML = "";
    updateAtributesDate();
    generateCalendar();
    updateSelectors();
    monthSelected.value = currentMonth;
    yearSelected.selectedIndex = 0;
}