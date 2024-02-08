from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from dateutil import parser

from datetime import timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime as dt
import os.path
import json

@method_decorator(csrf_exempt, name='dispatch')
class IndexView(TemplateView):
    template_name = 'shift/index.html'


SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = './json_google/credential_calendar.json'

def get_google_calendar_events(selected_date):
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

        next_day = dt.datetime.strptime(selected_date, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(days=1)
        next_day_str = next_day.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Call the Calendar API
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=selected_date,
                timeMax=next_day_str,
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
            formatted_start = parser.parse(start).strftime("%Y-%m-%d %H:%M:%S %p %Z")
            event_data = {
                "event": event["summary"],
                "formatted_start": formatted_start
            }
            response.append(event_data)
            
        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return response

@csrf_exempt
def get_list_dates(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_date = data.get('date')
        print("selected_date es {}".format(selected_date),flush=True)
        events = get_google_calendar_events(selected_date)

        return JsonResponse({'events': events})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

#def solicitud_turno(request):
    # google_calendar_events = get_google_calendar_events()

    # return render(request, 'turnos/solicitud_turno.html', {'events': google_calendar_events})