import random
import string
import os
import re
from datetime import datetime

from django.core.mail import send_mail
from applications.person.models import Person
from applications.shift.models import Shift
from applications.state.models import State
from app.settings.base import EMAIL_HOST_USER

def person_exists(email):
    person = Person.objects.filter(email=email)
    if person:
        return True
    return False

def create_person(email, first_name, last_name):
    Person.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

def create_shift(selected_date_time, email, confirmation_code, cancelation_url):
    person_instance = Person.objects.get(email=email)
    split_selected_date = selected_date_time.split()
    shift = Shift.objects.create(
        date=split_selected_date[0],
        hour=split_selected_date[1],
        id_person=person_instance,
        id_state=State.objects.get(short_description="pendiente"),
        confirmation_code=confirmation_code,
        confirmation_url=cancelation_url
    )
    
    return shift

def count_pending_shifts(email):
    from .models import Shift
    from applications.state.models import State
    pending_state_id = State.objects.filter(short_description="pendiente").values_list('id', flat=True).first()

    pending_shifts_count = Shift.objects.filter(id_person__email=email, id_state=pending_state_id).count()

    return pending_shifts_count

def is_mail(mail):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, mail):
        return True
    else:
        return False    
#Le enviamos un mail al cliente indicando que se ha recibido el turno. 
def send_mail_to_receiver(user, shift, is_receiver):
    if is_receiver:
        URL = os.environ.get('NGROK_URL', 'http://localhost:8000')
        sender = EMAIL_HOST_USER
        receiver = shift.id_person.email
        asunto = "Respuesta de solicitud de turno."
        message = ("Su solicitud de turno ha sido " +
           shift.id_state.short_description +
           " por el usuario " + user.username + ".\n\n")
        if shift.id_state.short_description == "confirmado":
            message += ("Su código de verificación es " + shift.confirmation_code +
                        ", podra ingresarlo en la web " + 
                        URL + "/shift/home/" +
                        " para recordar su turno en caso de ser necesario.\n" +
                        "En caso de querer cancelar su turno, puede hacerlo ingresando al siguiente enlace:\n" +
                        shift.confirmation_url + "\n\n" +
                        "Recuerde que debe hacerlo dos días previo al turno programado.\n\n" +
                        "Gracias, saludos!")
        else:
            message += ("Si desea puede volver a solicitar su turno, para ello ingrese a la url " +
                        URL + ".\n"+
                        "Gracias, saludos!")
    else:
        person = Person.objects.get(id_user=user.id)
        date_str = shift.date.strftime('%d/%m/%Y')
        hour_str = shift.hour.strftime('%H:%M:%S')
        sender = shift.id_person.email
        receiver = person.email
        asunto = "Canecelación de turno."
        message = ( shift.id_person.last_name + " " + shift.id_person.first_name +
                    " ha cancelado el turno que contaba para el día " +
                date_str + " a las " + hour_str +"hs" + ".\n"
                "Su email es "+ shift.id_person.email +".\n\n")
        if shift.description != "":
            message +=  ("Manifestó: '" + shift.description + "'.\n\n")            
           
    send_mail(asunto, message, sender, [receiver,])
    
#Le enviamos un mail al operador indicando que se ha cancelado un turno.
def send_mail_to_operator(user_mail, shift):
    asunto = shift.id_person.last_name + " " + shift.id_person.first_name + " ha cancelado el turno."
    date_str = shift.date.strftime('%d/%m/%Y')
    hour_str = shift.hour.strftime('%H:%M:%S')
    message = shift.id_person.last_name + " " + shift.id_person.first_name + " ha cancelado el turno" \
            " que tenia confirmado para el dia " + date_str + " en el horario " + hour_str + "hs."
    
    send_mail(asunto, message, EMAIL_HOST_USER, [user_mail,])
    
def generate_confirmation_code(length=15):
    characters = string.ascii_letters + string.digits
    confirmation_code = ''.join(random.choice(characters) for i in range(length))
    return confirmation_code