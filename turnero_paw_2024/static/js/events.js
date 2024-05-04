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
    const formattedDate = selectedDate.toISOString();
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
        setTimeout(() => window.location.reload(), 5000);
    });
}