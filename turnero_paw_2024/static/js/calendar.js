import {
    getClassDay
} from './helpers.js';

export function generateCalendar(calendarBody, firstDayWeek, daysWeek, currentDay, thisMonth) {
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

export function updateAtributesDate(){
    if(currentMonth == thisMonth){
        currentDay = date.getDate();
    }
    firstDayMonth = new Date(currentYear, currentMonth, 1);
    lastDayMonth = new Date(currentYear, currentMonth + 1, 0);
    daysWeek = lastDayMonth.getDate();
    firstDayWeek = firstDayMonth.getDay();
}

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
