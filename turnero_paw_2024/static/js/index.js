let date = new Date();

export const thisYear = date.getFullYear();
export const thisMonth = date.getMonth();
export const lastMonthShow = thisMonth + 2;
export const thisDay = date.getDate();

export let currentYear = date.getFullYear();
export let currentMonth = date.getMonth();
export let currentDay = date.getDate();

export let firstDayMonth = new Date(currentYear, currentMonth, 1);
export let lastDayMonth = new Date(currentYear, currentMonth + 1, 0);

export let daysWeek = lastDayMonth.getDate();
export let firstDayWeek = firstDayMonth.getDay();

export let calendarBody = document.getElementById("calendario-cuerpo");
export let monthSelected = document.getElementById("selectMonth");
export let yearSelected = document.getElementById("selectYear");

export let responseEvents = [];

export function setCurrentDay(newDay) {
    currentDay = newDay;
}

export function setResponseEvents(rspEvent) {
    responseEvents = rspEvent;
}

export function setFirstDayMonth(newFirstDay) {
    firstDayMonth = newFirstDay;
}

export function setlastDayMonth(newLastDayMonth) {
    lastDayMonth = newLastDayMonth;
}

export function setDaysWeek(newDaysWeek) {
    daysWeek = newDaysWeek;
}

export function setnFirstDayWeek(newFirstDayWeek) {
    firstDayWeek = newFirstDayWeek;
}

export function setCurrentMonth(newCurrentMonth) {
    currentMonth = newCurrentMonth;
}

export function setCurrentYear(newCurrentYear) {
    currentYear = newCurrentYear;
}

import {
    generateCalendar,
} from './calendar.js';

import {
    updateSelectors
} from './selectors.js';

import {
    setCurrentDate,
    changeMonth
} from './helpers.js';

const prevMonthButton = document.getElementById('prevMonth');
const nextMonthButton = document.getElementById('nextMonth');
const selectMonth = document.getElementById('selectMonth');
const selectYear = document.getElementById('selectYear');

prevMonthButton.addEventListener('click', () => changeMonth(-1));
nextMonthButton.addEventListener('click', () => changeMonth(1));

selectMonth.addEventListener('change', () => {
    console.log("Selecting month",selectMonth.value)
    const selectedMonthIndex = selectMonth.value;
    changeMonth(selectedMonthIndex - currentMonth);
});

selectYear.addEventListener('change', () => {
    const selectedYear = selectYear.value;
    setCurrentYear(selectedYear);
    generateCalendar();
});

generateCalendar();

updateSelectors();

setCurrentDate();