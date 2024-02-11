import {
    thisMonth,
    lastMonthShow,
    currentYear,
    currentMonth,
    currentDay,
    setCurrentDay,
    firstDayMonth,
    lastDayMonth,
    daysWeek,
    firstDayWeek,
    monthSelected,
    yearSelected,
    calendarBody
} from './index.js';

import {
    getClassDay
} from './helpers.js';

import {
    getGoogleCalendarEvents
} from './events.js';

export function generateCalendar() {
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
                cell.classList.add(getClassDay(day, thisMonth));

                if (day >= currentDay) {
                    cell.addEventListener("click", createClickHandler(day));
                }
                    
                day++;
            }
        }
    }
}

function createClickHandler(day) {
    return function() {
        const days = document.querySelectorAll('td');
        days.forEach(d => d.classList.remove('selected'));

        setCurrentDay(day);
        this.classList.add('selected');
        getGoogleCalendarEvents();
    };
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

document.addEventListener('DOMContentLoaded', function() {
    const closeButton = document.getElementById('modal-form-content-close-btn');
    if (closeButton) {
        closeButton.addEventListener('click', closeModal);
    }
});

export function changeMonth(value) {
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
