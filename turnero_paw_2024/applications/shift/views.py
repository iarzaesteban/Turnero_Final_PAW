import datetime as dt
import os.path
import re
import json
import random
from dateutil import parser
from collections import defaultdict
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Min, Max
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from google.auth.exceptions import RefreshError
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import helpers
from .forms import CancelShiftForm
from applications.shift.models import Shift
from applications.state.models import State
from applications.person.models import Person
from applications.user.models import Users
from app.settings.base import EMAIL_HOST_USER



@method_decorator(csrf_exempt, name='dispatch')
class IndexView(TemplateView):
    template_name = 'shift/index.html'


SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = './json_google/credential_keyss.json'

def get_credentials():
    creds = None
    
    # Carga las credenciales de la cuenta de servicio desde el archivo JSON
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
   
    return creds

def get_google_calendar_events(selected_date):
    creds = None
    
    try:
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        creds = get_credentials()
        events_get = []
        service = build("calendar", "v3", credentials=creds)

        next_day = dt.datetime.strptime(selected_date, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(days=1)
        next_day_str = next_day.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # Call the Calendar API
        # Nos traemos los eventos del día
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=selected_date,
                timeMax=next_day_str,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
                timeZone="America/Argentina/Buenos_Aires"
            )
            .execute()
        )
        events = events_result.get("items", [])
        start_end_times = Users.objects.aggregate(
            earliest_start_time=Min('start_time_attention'),
            latest_end_time=Max('end_time_attention')
        )
        
        start_time_attention = start_end_times['earliest_start_time']
        end_time_attention = start_end_times['latest_end_time']
        start_time_attention_user = start_time_attention.strftime("%H:%M")
        end_time_attention_user = end_time_attention.strftime("%H:%M")
        
        if not events:
            return {"events_get":events_get,
                    "start_time_attention_user": start_time_attention_user,
                    "end_time_attention_user": end_time_attention_user}
        
        start_time_count = defaultdict(int)
        # Armamos diccionario con la hora y la cantidad de veces que se repite ese horario
        for event in events:
            start_time = event["start"].get("dateTime", event["start"].get("date"))
            start_time_count[start_time] += 1
        #obtenemos los usuarios activos
        count_users_attentions = Users.objects.filter(has_set_attention_times=True)
        # Devolvemos de todos los eventos los que el front debe ocultar
        for start_time, count in start_time_count.items():
            formatted_start = parser.parse(start_time).strftime("%Y-%m-%d %H:%M:%S %p %Z")
            # Verificamos que si ya tenemos el mismo horario seteado para los horarios de atencion de 
            # los todos operadores 
            if count == count_users_attentions.count():
                event_data = {
                    "formatted_start": formatted_start
                }
                events_get.append(event_data)
            else:
                # Verificamos cauntos operadores pueden atender en cierto horario.
                count_hour_attention_user = 0
                for operator in count_users_attentions:
                    start_time_attention = operator.start_time_attention
                    end_time_attention = operator.end_time_attention
                    formatted_start_hour = parser.parse(start_time)
                    if formatted_start_hour.time() >= start_time_attention and formatted_start_hour.time() <= end_time_attention:
                        count_hour_attention_user +=1
                if count_hour_attention_user < count_users_attentions.count():
                    event_data = {
                        "formatted_start": formatted_start
                    }
                    events_get.append(event_data)
                
        return {"events_get":events_get,
                "start_time_attention_user": start_time_attention_user,
                "end_time_attention_user": end_time_attention_user}

    
    except FileNotFoundError as e:
        return {
            "error": "No se encontró el archivo de credenciales. Por favor, contacte al administrador."
        }
    except HttpError as e:
        return {
            "error": "Hubo un problema al acceder a Google Calendar. Inténtelo más tarde."
        }
    except Exception as e:
        return {
            "error": f"Error inesperado: {str(e)}"
        }

def add_event_to_google_calendar(event_summary, event_description, start_datetime, end_datetime):
    event_timezone = 'America/Argentina/Buenos_Aires'
    creds = get_credentials()
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

def delete_event_from_google_calendar(event_id):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return False

def remove_event_from_google_calendar(day, hour, id):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    selected_datetime = datetime.combine(day, hour)

    time_min = selected_datetime.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    time_max = (selected_datetime + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'

    try:
        events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max).execute()
        events = events_result.get('items', [])
        for event in events:
            shift_id = json.loads(event['summary']).get('shift_id')
            if shift_id and shift_id == id:
                return delete_event_from_google_calendar(event['id'])

        return False

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False

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
        # Verificamos que el cliente no tenga mas de 2 turnos solicitados en estado pendiente
        if helpers.count_pending_shifts(email) >= 2:
            return JsonResponse({
                    'response': "error", 
                    "message": "La persona ya tiene más de 1 turno en estado pendiente"} )
        
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
        obj_date = datetime.strptime(shift.date, '%Y-%m-%d')
        format_date = obj_date.strftime('%d/%m/%Y')
        shift_data = {
            'day': format_date,
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
        return render(request, 'shift/shift_details_before_cancel.html', {'shift': shift})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def send_confirmation_code(shift):
    code = str(random.randint(100000, 999999))
    shift.verification_code = code
    shift.save()
    helpers.send_mails(
        'Código de Confirmación de Cancelación de Turno',
        f'{code}',
        EMAIL_HOST_USER,
        shift.id_person.email,
    )

@csrf_exempt
def initiate_cancel_shift(request):
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')
        shift = get_object_or_404(Shift, confirmation_code=confirmation_code)
        send_confirmation_code(shift)
        return JsonResponse({'success': True, 'shift_id': shift.id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def confirm_cancel_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        form = CancelShiftForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')
            cancel_description = form.cleaned_data.get('cancel_description')
            if shift.id_state.short_description != "cancelado":
                if verification_code:
                    if shift.verification_code == verification_code:
                        shift.id_state = State.objects.get(short_description='cancelado')
                        shift.save()
                        helpers.send_mail_to_receiver(shift.id_user, shift, False)
                        remove_event_from_google_calendar(shift.date, shift.hour, shift.id)
                        return render(request, 'shift/confirm_cancel.html', {
                            'success_message': 'Se ha cancelado el turno de forma exitosa.',
                            'set_description': False,
                            'shift': shift,
                            'form': form
                        })
                    else:
                        return render(request, 'shift/confirm_cancel.html', {
                            'error': 'Código incorrecto',
                            'set_description': False,
                            'shift': shift,
                            'form': form
                        })

                if cancel_description:
                    if not re.match(r'^[a-zA-Z0-9\s.,/!?áéíóúÁÉÍÓÚñÑüÜ]+$', cancel_description):
                        return render(request, 'shift/confirm_cancel.html', {
                            'success_message': 'Se ha cancelado el turno de forma exitosa.',
                            'error': 'La descripción contiene caracteres no permitidos.',
                            'set_description': False,
                            'shift': shift,
                            'form': form
                        })
                    shift.description = cancel_description
                    shift.save()
                    return render(request, 'shift/confirm_cancel.html', {
                        'success_message': 'Se ha agregado la descripción al turno de forma exitosa.', 
                        'shift': shift,
                        'set_description': True,
                        'form': form
                    })

                if not cancel_description:
                    return render(request, 'shift/confirm_cancel.html', {
                        'success_message': 'Se ha cancelado el turno de forma exitosa.',
                        'set_description': True,
                        'shift': shift,
                        'form': form
                    })
            else:
                return render(request, 'shift/shift_details_before_cancel.html', {'shift': shift})

    else:
        form = CancelShiftForm()
    if shift.id_state.short_description != "cancelado":
        return render(request, 'shift/confirm_cancel.html', {'shift': shift, 'form': form})
    else:
        return render(request, 'shift/shift_details_before_cancel.html', {'shift': shift})


def serialize_shifts(page_obj):
    return [{'date': shift.date,
            'hour': shift.hour,
            'full_name': shift.id_person.last_name + " " + shift.id_person.first_name,
            'mail': shift.id_person.email,
            'id_person': str(shift.id_person),} for shift in page_obj]
    
@login_required
def get_shifts_today(request):
    state = request.GET.get('state')
    title = f"Turnos {state}s para hoy"
    today = datetime.now()
    list_shift = {}
    if state == "confirmado":
        list_shift = Shift.objects.filter(
                                date=today,
                                id_user=request.user.id, 
                                id_state__short_description=state).order_by("hour")
    else:
        list_shift = Shift.objects.filter(
                                date=today,
                                id_state__short_description=state).order_by("hour")
        
        
    paginator = Paginator(list_shift, 5)
    page_number = request.GET.get("page")
    try:
        list_shift = paginator.page(page_number)
    except PageNotAnInteger:
        list_shift = paginator.page(1)
    except EmptyPage:
        list_shift = paginator.page(paginator.num_pages)
    return render(request, 'user/today_shifts_states.html', {'list_shift': list_shift, 
                                                             'title': title,
                                                             'state': state})

class ConfirmShiftView(LoginRequiredMixin, View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        user = self.request.user
        try:
            if shift.id_user:
                if user != shift.id_user:
                    shift.id_user = user
                    shift.save()
                    return redirect('home-user')
            confirmed_state = State.objects.get(short_description='confirmado')
            shift.id_state = confirmed_state
            shift.id_user = user
            shift.save()
            helpers.send_mail_to_receiver(user, shift, True)
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
    def post(self, request, shift_id):
        data = json.loads(request.body)
        description = data.get('description', '')
        shift = Shift.objects.filter(id=shift_id).first() 
        try:
            canceled_state = State.objects.get(short_description='cancelado')
            shift.id_state = canceled_state
            shift.description = description
            shift.save()
            remove_event_from_google_calendar(shift.date, shift.hour, shift.id)
            helpers.send_mail_to_receiver(shift.id_user, shift, False)
            return JsonResponse({'redirect_url': '/shift/home/'})
            
        except State.DoesNotExist:
            error_message = 'Estado de turno no encontrado'
            return JsonResponse({'error_message': error_message}, status=400)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'error_message': error_message}, status=500)

    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        
        try:
            canceled_state = State.objects.get(short_description='cancelado')
            shift.id_state = canceled_state
            remove_event_from_google_calendar(shift.date, shift.hour, shift.id)
            if not isinstance(self.request.user, AnonymousUser):
                user = self.request.user
                shift.id_user = user
                shift.save()
                helpers.send_mail_to_receiver(user, shift, True)
                return redirect('home-user')
            shift.save()
            person = Person.objects.get(id_user=shift.id_user)
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
        
class CompleteShiftView(LoginRequiredMixin, View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        try:
            complete_state = State.objects.get(short_description='completado')
            now = timezone.now()
            shift_datetime = timezone.make_aware(datetime.combine(shift.date, shift.hour))
            if shift_datetime > now:
                error_message = 'No puedes completar un turno que aún no ha ocurrido.'
                if not isinstance(self.request.user, AnonymousUser):
                    list_shift = Shift.objects.filter(id_state__short_description='confirmado')
                    return render(request, 'user/home_user.html', {
                                                    'list_shift': list_shift, 
                                                    'error_message': error_message})
            shift.id_state = complete_state
            if not isinstance(self.request.user, AnonymousUser):
                user = self.request.user
                shift.id_user = user
                shift.save()
                return redirect('get-confirm-shifts-today')
            shift.save()
            
            return redirect('get-confirm-shifts-today')
        except State.DoesNotExist:
            if not isinstance(self.request.user, AnonymousUser):
                list_shift = Shift.objects.filter(id_state__short_description='confirmado')
                error_message = 'Estado de turno no encontrado'
                return render(request, 'user/home_user.html', {
                                                    'list_shift': list_shift, 
                                                    'error_message': error_message})
            return redirect('get-confirm-shifts-today')
        except Exception as e:
            if not isinstance(self.request.user, AnonymousUser):
                list_shift = Shift.objects.filter(id_state__short_description='confirmado')
                error_message = str(e)
                return render(request, 'user/home_user.html', {
                                                        'list_shift': list_shift, 
                                                        'error_message': error_message})
            return redirect('get-confirm-shifts-today')
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
                'state': shift.id_state.description,
                'email': shift.id_person.email,
            }
            return JsonResponse({'turno_detalle': turno_detalle})
        else:
            return JsonResponse({'error': 'No se encontró ningún turno con ese código de confirmación.'})
    