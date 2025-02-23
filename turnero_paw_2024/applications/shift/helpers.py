import datetime as dt
import random
import json
import string
import os
import re
from datetime import timedelta, datetime
from collections import defaultdict
from dateutil import parser

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from applications.person.models import Person
from applications.user.models import Users
from app.settings.base import EMAIL_HOST_USER

from .constants import CREDENTIALS_FILE, SCOPES

from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

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
        start_end_times = Users.get_min_max_time_attentions_users()
        
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
        count_users_attentions = Users.get_users_with_attentions_times()
        # Devolvemos de todos los eventos los que el front debe ocultar
        for start_time, count in start_time_count.items():
            formatted_start = parser.parse(start_time).strftime("%Y-%m-%d %H:%M:%S %p %Z")
            # Verificamos que si ya tenemos el mismo horario seteado para los horarios de atencion de 
            # todos los operadores 
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
    

def send_confirmation_code(shift):
    code = str(random.randint(100000, 999999))
    shift.verification_code = code
    shift.save()
    send_mails(
        'Código de Confirmación de Cancelación de Turno',
        f'{code}',
        EMAIL_HOST_USER,
        shift.id_person.email,
    )


def is_mail(mail):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, mail):
        return True
    else:
        return False

def send_mails(asunto, code, sender, receiver):
    sub_title = "Código de verificación"
    formatted_code = ''.join([f'<span class="digit">{digit}</span>' for digit in code])
    message = f'<p>{formatted_code}</p>'
    html_content = render_to_string('shift/email_template.html', {'sub_title': sub_title, 'message': message})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(asunto, text_content, sender, [receiver])
    email.attach_alternative(html_content, "text/html")
    email.send()

#Le enviamos un mail al cliente indicando que se ha recibido el turno. 
def send_mail_to_receiver(user, shift, is_receiver):
    date_str = shift.date.strftime('%d/%m/%Y')
    hour_str = shift.hour.strftime('%H:%M:%S')
    sub_title = "Turno " + shift.id_state.short_description
    if is_receiver:
        URL = os.environ.get('NGROK_URL', 'http://localhost:8000')
        sender = EMAIL_HOST_USER
        receiver = shift.id_person.email
        asunto = "Respuesta de solicitud de turno."
        message = ("Su solicitud de turno para el día "+ date_str +" a las "+ hour_str +
                   "hs ha sido <strong>" +  shift.id_state.short_description +
                    "</strong> por el operador " + user.username + ".<br><br>")
        if shift.id_state.short_description == "confirmado":
            message += ("Su código de verificación es <strong>" + shift.confirmation_code +
                        "</strong>, podrá ingresarlo en la " + 
                        "<a href='" + URL + "/shift/home/" + "' > "+
                        "web</a> para recordar su turno en caso de ser necesario.<br>" +
                        "En caso de necesitar cancelar su turno, puede hacerlo ingresando " +
                        "<a href='" + shift.confirmation_url + "' > "+
                        "aquí</a> <br><br>" +
                        "Recuerde que debe hacerlo dos días previo al turno programado.<br><br>" +
                        "Gracias, saludos!")
        else:
            message += ("Si desea puede volver a solicitar un nuevo turno, para ello ingrese " +
                        "<a href='" + URL + "/shift/home/" + "' > "+
                        "aquí</a> <br><br>" +
                        "Gracias, saludos!")
    else:
        person = Person.objects.get(id_user=user.id)
        sender = shift.id_person.email
        receiver = person.email
        asunto = "Cancelación de turno."
        message = ( shift.id_person.last_name + " " + shift.id_person.first_name +
                    " ha cancelado el turno que contaba para el día " +
                date_str + " a las " + hour_str +"hs" + ".<br>"
                "Su email es "+ shift.id_person.email +".<br><br>")
        if shift.description != "":
            message +=  ("Manifestó: '" + shift.description + "'.<br><br>")            
           
    html_content = render_to_string('shift/email_template.html', {'sub_title': sub_title, 'message': message})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(asunto, text_content, sender, [receiver])
    email.attach_alternative(html_content, "text/html")
    email.send()
    #send_mail(asunto, message, sender, [receiver,])
    
#Le enviamos un mail al operador indicando que se ha cancelado un turno.
def send_mail_to_operator(user_mail, shift):
    asunto = shift.id_person.last_name + " " + shift.id_person.first_name + " ha cancelado el turno."
    date_str = shift.date.strftime('%d/%m/%Y')
    hour_str = shift.hour.strftime('%H:%M:%S')
    message = shift.id_person.last_name + " " + shift.id_person.first_name + " ha cancelado el turno" \
            " que tenia confirmado para el dia " + date_str + " en el horario " + hour_str + "hs."
    
    html_content = render_to_string('shift/email_template.html', {'message': message})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(asunto, text_content, EMAIL_HOST_USER, [user_mail,])
    email.attach_alternative(html_content, "text/html")
    email.send()
    send_mail(asunto, message, EMAIL_HOST_USER, [user_mail,])
    
def generate_confirmation_code(length=15):
    characters = string.ascii_letters + string.digits
    confirmation_code = ''.join(random.choice(characters) for i in range(length))
    return confirmation_code


def serialize_shifts(page_obj):
    return [{'date': shift.date,
            'hour': shift.hour,
            'full_name': shift.id_person.last_name + " " + shift.id_person.first_name,
            'mail': shift.id_person.email,
            'id_person': str(shift.id_person),} for shift in page_obj]