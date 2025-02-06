import datetime
from io import BytesIO
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from PIL import Image
from .models import Users
from applications.person.models import Person
from applications.shift.models import Shift
from applications.aditional_information.models import AditionalInformation
from app.settings.base import EMAIL_HOST_USER
from .helpers import generate_confirmation_code
from .constants import PENDING_SHIFT

def authenticate_and_login_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    return user


def create_user(form_data):
    """Crea un usuario y una persona asociados."""
    # Validar contraseñas
    password = form_data.get('password')
    confirm_password = form_data.get('confirm_password')
    if password != confirm_password:
        raise ValueError('Las contraseñas no coinciden')

    # Validar username y email
    username = form_data.get('username')
    if Users.objects.filter(username=username).exists():
        raise ValueError('El usuario ingresado ya está en uso')
    
    email = form_data.get('email')
    if Person.objects.filter(email=email).exists():
        raise ValueError('Este correo electrónico ya está en uso')

    # Procesar imagen
    picture = form_data.get('picture')
    output = BytesIO()
    if picture:
        img = Image.open(picture)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(output, format='JPEG', quality=70)

    # Crear usuario
    verification_code = generate_confirmation_code()
    user = Users.objects.create_user(
        username=username,
        password=password,
        code_verification=verification_code,
        picture=output.getvalue()
    )

    # Crear persona
    person = Person.objects.create(
        first_name=form_data.get('first_name'),
        last_name=form_data.get('last_name'),
        email=email,
        id_user=user
    )

    return user, person


def send_verification_email(user, person, current_user=None):
    """Envía un correo electrónico con el código de verificación."""
    date = datetime.datetime.now()
    date_str = date.strftime('%d-%m-%Y %H:%M')
    asunto = "Confirmación de correo"
    message = (
        f"El código de verificación es {user.code_verification}. "
        f"La hora es {date_str}."
    )
    recipient = [person.email] if current_user else [person.email, EMAIL_HOST_USER]
    send_mail(asunto, message, EMAIL_HOST_USER, recipient)


def get_pending_shifts_paginate():
    pending_shifts = Shift.objects.filter(id_state__short_description='pendiente',
                                              date__gte=datetime.date.today()).order_by('date','hour')
    paginator = Paginator(pending_shifts, 5)
    return pending_shifts, paginator


def active_user(id):
    Users.objects.filter(id=id).update(is_active=True)


def get_aditional_information():
    return AditionalInformation.objects.all()


def create_aditional_information(form):
    title = form.cleaned_data['title']
    description = form.cleaned_data['description']
    link = form.cleaned_data['link']
    icon_base64 = form.cleaned_data['icon_base64']            
    
    AditionalInformation.objects.create(
        title=title,
        description=description,
        link=link,
        icon=icon_base64
    )


def get_shifts_user_confirm(username, only_today):
    if only_today:
        return Shift.objects.filter(
                                id_user__username=username, 
                                id_state__short_description='confirmado',
                                date=datetime.date.today())


    return Shift.objects.filter(
                        id_user__username=username, 
                        id_state__short_description='confirmado',
                        date__gte=
                        datetime.date.today()).order_by('date', 'hour')


def get_pending_shifts(order_by):
    if order_by is not None:
        return Shift.objects.filter(id_state__short_description=PENDING_SHIFT).order_by(order_by)
    return Shift.objects.filter(id_state__short_description=PENDING_SHIFT)


def get_confirms_shifts_today(date, order_by):
    return Shift.objects.filter(id_state__short_description="confirmado",
                            date=date).order_by(order_by)

def make_pagination(data, number_rows):
    return Paginator(data, number_rows)


def get_rest_users_actives(exclude_user):
    return  Users.objects.exclude(
                username=exclude_user.username
            ).exclude(
                start_time_attention__isnull=True
            ).exclude(
                end_time_attention__isnull=True
            )