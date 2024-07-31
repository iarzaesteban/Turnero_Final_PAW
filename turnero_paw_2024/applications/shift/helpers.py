import random
import string
import os
import re
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
    if is_receiver:
        URL = os.environ.get('NGROK_URL', 'http://localhost:8000')
        sender = EMAIL_HOST_USER
        receiver = shift.id_person.email
        asunto = "Respuesta de solicitud de turno."
        sub_title = "Turno " + shift.id_state.short_description
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
    #send_mail(asunto, message, EMAIL_HOST_USER, [user_mail,])
    
def generate_confirmation_code(length=15):
    characters = string.ascii_letters + string.digits
    confirmation_code = ''.join(random.choice(characters) for i in range(length))
    return confirmation_code