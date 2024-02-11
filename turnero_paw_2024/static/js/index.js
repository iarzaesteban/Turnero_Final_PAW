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

import {
    generateCalendar,
} from './calendar.js';

import {
    updateSelectors
} from './selectors.js';

import {
    setCurrentDate
} from './helpers.js';

generateCalendar();

updateSelectors();

setCurrentDate();