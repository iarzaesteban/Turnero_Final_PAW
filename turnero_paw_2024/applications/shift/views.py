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
from django.contrib.auth.models import AnonymousUser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import helpers
from app.settings.base import EMAIL_HOST_USER
from applications.shift.models import Shift
from applications.state.models import State
from applications.person.models import Person

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
        
        if helpers.count_pending_shifts(email) >= 2:
            return JsonResponse({'response': "error", "message": "La persona ya tiene más de 1 turno en estado pendiente"} )
        
        if not helpers.person_exists(email):
            helpers.create_person(email, first_name, last_name)

        confirmation_code = helpers.generate_confirmation_code()
        cancelation_url = request.build_absolute_uri(reverse('cancel_shift')) + f'?confirmation_code={confirmation_code}'
        shift = helpers.create_shift(selected_date_time, email, confirmation_code, cancelation_url)
        
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
        
        # shift.delete() 
        return render(request, 'shift/shift_details_before_cancel.html', {'shift': shift})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_shifts_today(request):
    today = datetime.now()
    print("TODAY IS {}".format(today), flush=True)
    shifts_today = Shift.objects.filter(date=today, id_user=request.user, id_state__short_description='confirmado')

    shifts_list = []
    for shift in shifts_today:
        shifts_list.append({
            'date': shift.date,
            'hour': shift.hour,
            'full_name': shift.id_person.last_name + " " + shift.id_person.first_name,
            'mail': shift.id_person.email,
            'id_person': str(shift.id_person),
        })
    return JsonResponse({'shifts_today': shifts_list})


class ConfirmShiftView(View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        user = self.request.user
        try:
            print("shift.id_user {}".format(shift.id_user), flush=True)
            print("user != shift.id_user {}".format(user != shift.id_user), flush=True)
            if shift.id_user:
                if user != shift.id_user:
                    shift.id_user = user
                    shift.save()
                    return redirect('home-user')
            confirmed_state = State.objects.get(short_description='confirmado')
            shift.id_state = confirmed_state
            shift.id_user = user
            shift.save()
            helpers.send_mail_to_user(user, shift)
            return redirect('home-user')
        except State.DoesNotExist:
            pending_shifts = Shift.objects.filter(id_state__short_description='pendiente')
            error_message = 'Estado de turno no encontrado'
            return render(request, 'user/home_user.html', {'pending_shifts': pending_shifts, 'error_message': error_message})
        except Exception as e:
            pending_shifts = Shift.objects.filter(id_state__short_description='pendiente')
            error_message = str(e)
            return render(request, 'user/home_user.html', {'pending_shifts': pending_shifts, 'error_message': error_message})

class CancelShiftView(View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        
        try:
            print("ID USER ES {}".format(self.request.user),flush=True)
            canceled_state = State.objects.get(short_description='cancelado')
            shift.id_state = canceled_state
            if not isinstance(self.request.user, AnonymousUser):
                print("Entro al user if", flush=True)
                user = self.request.user
                shift.id_user = user
                shift.save()
                helpers.send_mail_to_receiver(user, shift)
                return redirect('home-user')
            print("ANTES DEL SAVE",flush=True)
            shift.save()
            print("DESPUES DEL SAVE",flush=True)
            person = Person.objects.get(id_user=shift.id_user)
            print("ID PERsON ES {}".format(person),flush=True)
            helpers.send_mail_to_operator(person.email, shift)
            return redirect('/shift/home/')
        except State.DoesNotExist:
            if not isinstance(self.request.user, AnonymousUser):
                pending_shifts = Shift.objects.filter(id_state__short_description='pendiente')
                error_message = 'Estado de turno no encontrado'
                return render(request, 'user/home_user.html', {'pending_shifts': pending_shifts, 'error_message': error_message})
            return redirect('/shift/home/')
        except Exception as e:
            if not isinstance(self.request.user, AnonymousUser):
                pending_shifts = Shift.objects.filter(id_state__short_description='pendiente')
                error_message = str(e)
                return render(request, 'user/home_user.html', {'pending_shifts': pending_shifts, 'error_message': error_message})
            return redirect('/shift/home/')
    
class SearchShiftsView(View):
    def get(self, request):
        search_value = request.GET.get('search_value', '')
        shift = None
        if helpers.is_mail(search_value):
            person = Person.objects.filter(email=search_value).first()
            if person:
                shift = Shift.objects.filter(id_person=person.id).first()
        else:
            shift = Shift.objects.filter(confirmation_code=search_value).first()
        
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
    