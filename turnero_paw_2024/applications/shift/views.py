import datetime as dt
import os.path
import json
from dateutil import parser
from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .helpers import person_exists, create_person, create_shift, generate_confirmation_code, count_pending_shifts

from applications.shift.models import Shift
from applications.state.models import State

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
        return response

def add_event_to_google_calendar(event_summary, event_description, start_datetime, end_datetime):
    event_timezone = 'America/Argentina/Buenos_Aires'

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': event_summary,
        'description': event_description,
        'start': {
            'dateTime': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': event_timezone,
        },
        'end': {
            'dateTime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': event_timezone,
        },
        'reminders': {
            'useDefault': False,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event


@csrf_exempt
def get_list_dates(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_date = data.get('date')
        events = get_google_calendar_events(selected_date)

        return JsonResponse({'events': events})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def confirm_shift(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        first_name = data.get('name')
        last_name = data.get('last_name')
        selected_date_time = data.get('dateTime')
        
        if count_pending_shifts(email) >= 2:
            return JsonResponse({'response': "error", "message": "La persona ya tiene más de 1 turno en estado pendiente"} )
        
        if not person_exists(email):
            create_person(email, first_name, last_name)

        confirmation_code = generate_confirmation_code()
        #cancelation_date = parser.parse(selected_date).date() - timedelta(days=2)
        cancelation_url = request.build_absolute_uri(reverse('cancel_shift')) + f'?confirmation_code={confirmation_code}'
        shift = create_shift(selected_date_time, email, confirmation_code, cancelation_url)
        
        event_data = {
            'shift_id': shift.id,
            'person_name': f"{shift.id_person.last_name} {shift.id_person.first_name}"
        }
        event_summary = json.dumps(event_data)
        event_description = f"Fecha: {shift.date}, Hora: {shift.hour}"
        shift_date = datetime.strptime(shift.date, '%Y-%m-%d').date()
        shift_time = datetime.strptime(shift.hour+":00", '%H:%M:%S').time()
        start_datetime = datetime.combine(shift_date, shift_time)  
        end_datetime = start_datetime + timedelta(minutes=30) 

        add_event_to_google_calendar(event_summary, event_description, start_datetime, end_datetime)
        shift_data = {
            'day': shift.date,
            'hour': shift.hour,
            'person': shift.id_person.last_name +" "+ shift.id_person.first_name,
        }
        return JsonResponse({'response': "ok", "shift": shift_data})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def cancel_shift(request):
    if request.method == 'GET':
        confirmation_code = request.GET.get('confirmation_code')
        shift = get_object_or_404(Shift, confirmation_code=confirmation_code)
        # Realiza cualquier lógica necesaria para cancelar el turno aquí
        shift.delete()  # Por ejemplo, aquí simplemente eliminamos el turno
        return JsonResponse({'message': 'Turno cancelado exitosamente'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


class ConfirmShiftView(View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        confirmed_state = State.objects.get(short_description='confirmado')
        shift.id_state = confirmed_state
        shift.save()
        return redirect('home-user')

class CancelShiftView(View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        canceled_state = State.objects.get(short_description='cancelado')
        shift.id_state = canceled_state
        shift.save()
        return redirect('home-user')
    
class BuscarTurnoView(View):
    def get(self, request):
        confirmation_code = request.GET.get('confirmation_code', '')
        shift = Shift.objects.filter(confirmation_code=confirmation_code).first()
        if shift:
            turno_detalle = {
                'date': shift.date,
                'hour': shift.hour,
                'first_name': shift.id_person.first_name,
                'last_name': shift.id_person.last_name,
                'email': shift.id_person.email,
            }
            return JsonResponse({'turno_detalle': turno_detalle})
        else:
            return JsonResponse({'error': 'No se encontró ningún turno con ese código de confirmación.'})