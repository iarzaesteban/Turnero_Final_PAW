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

import {
    generateCalendar,
    updateAtributesDate,
    changeMonth
} from './calendar.js';

import {
    openModal,
    closeModal
} from './modal.js';

import {
    cleanSelectors,
    updateSelectors
} from './selectors.js';

import {
    getGoogleCalendarEvents
} from './events.js';

import {
    getMonthName,
    setCurrentDay
} from './helpers.js';

generateCalendar(calendarBody, firstDayWeek, daysWeek, currentDay,thisMonth);

updateSelectors(monthSelected, yearSelected, thisMonth, currentYear);

setCurrentDay(currentYear, currentMonth, currentDay);