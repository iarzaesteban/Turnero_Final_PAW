import {
    currentYear,
    currentMonth,
    currentDay,
    setResponseEvents,
} from './index.js';

import {
    generateSchedules
} from './helpers.js';

export function getGoogleCalendarEvents() {
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
        setResponseEvents(data.events);
        generateSchedules();
    })
    .catch(error => {
        console.error('Error fetching Google Calendar events:', error);
    });
}