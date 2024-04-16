import {
    currentYear,
    currentMonth,
    currentDay,
    setResponseEvents,
    setResponseStartTimeAttention,
    setResponseEndTimeAttention,
} from './index.js';

import {
    generateSchedules
} from './helpers.js';

export function getGoogleCalendarEvents() {
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    console.log("selectedDate", selectedDate);
    const formattedDate = selectedDate.toISOString();
    console.log("formattedDate", formattedDate);
    fetch('/shift/get_google_calendar_events/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        
        body: JSON.stringify({ date: formattedDate}),
    })
    .then(response => response.json())
    .then(data => { 
        setResponseEvents(data.events.events_get);
        setResponseStartTimeAttention(data.events.start_time_attention_user);
        setResponseEndTimeAttention(data.events.end_time_attention_user);
        generateSchedules();
    })
    .catch(error => {
        console.error('Error fetching Google Calendar events:', error);
    });
}