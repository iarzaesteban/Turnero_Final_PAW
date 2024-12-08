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

const calendarContainer = document.getElementById('calendar-container');
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
        if (data.events.error) {
            const message = data.events.error;
            const existingMessage = document.querySelector('.message-request-shift');

            if (existingMessage) {
                calendarContainer.removeChild(existingMessage);
            }
            const messageRequestShift = document.createElement('p');
            messageRequestShift.textContent = message;
            messageRequestShift.classList.add('message-request-shift');

            const closeButton = document.createElement('span');
            closeButton.textContent = 'X';
            closeButton.style.cursor = 'pointer';
            closeButton.style.marginLeft = '10px';

            closeButton.addEventListener('click', function() {
                calendarContainer.removeChild(messageRequestShift);
            });
            
            messageRequestShift.appendChild(closeButton);
            const firstChild = calendarContainer.firstChild;
            calendarContainer.insertBefore(messageRequestShift, firstChild);
        }
        setResponseEvents(data.events.events_get);
        setResponseStartTimeAttention(data.events.start_time_attention_user);
        setResponseEndTimeAttention(data.events.end_time_attention_user);
        generateSchedules();
    })
}