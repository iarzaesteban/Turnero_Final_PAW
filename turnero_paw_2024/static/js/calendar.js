import {
    thisMonth,
    currentDay,
    setCurrentDay,
    daysWeek,
    firstDayWeek,
    calendarBody,
    currentMonth
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

                if (day >= currentDay || thisMonth != currentMonth) {
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


