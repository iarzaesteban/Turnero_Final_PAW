from django.shortcuts import render, redirect
from applications.turnos.forms import TurnoForm
from django.views.generic import TemplateView
import calendar
from datetime import datetime, timedelta
import datetime as dt
import os.path
from dateutil import parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = './json_google/credential_calendar.json'

def get_google_calendar_events():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        response = []
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = dt.datetime.utcnow().isoformat() + "Z" 
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        
        if not events:
            print("No upcoming events found.")
            return response
        
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            formatted_start = parser.parse(start).strftime("%Y-%m-%d %H:%M:%S %Z")
            event_data = {
                "event": event["summary"],
                "formatted_start": formatted_start
            }
            response.append(event_data)
            
        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return response

def solicitud_turno(request):
    google_calendar_events = get_google_calendar_events()
    mounths = ["Eenro", "Febrero", "Marzo",
               "Abril", "Mayo", "Junio", 
               "Julio", "Agosto", "Septiembre", 
               "Octubre", "Noviembre", "Diciembre"]
    days = ["Lunes", "Martes", "Miercoles", "Jueves",
             "Viernes", "Sabado", "Domingo"]
    today = datetime.now()
    days_in_current_month = calendar.monthrange(today.year, today.month)[1]
    days_in_next_month = calendar.monthrange(today.year, today.month+1)[1]
    days_in_two_month = calendar.monthrange(today.year, today.month+2)[1]
    day_names = list(calendar.day_name)
    start_day_name = day_names[datetime(today.year, today.month, 1).weekday()]

    return render(request, 'turnos/solicitud_turno.html', {'events': google_calendar_events,
                                                           'mounths': mounths,
                                                           'days': days,
                                                           'today': today,
                                                           'days_in_current_month': days_in_current_month,
                                                           'days_in_next_month': days_in_next_month,
                                                           'days_in_two_month': days_in_two_month,
                                                           'start_day_name': start_day_name})


class IndexView(TemplateView):
    template_name = 'turnos/solicitud_turno.html'
