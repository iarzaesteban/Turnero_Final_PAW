import datetime
from io import BytesIO
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from PIL import Image
from .models import Users
from applications.person.models import Person
from applications.shift.models import Shift
from app.settings.base import EMAIL_HOST_USER
from .helpers import generate_confirmation_code

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

def get_pending_shifts():
    pending_shifts = Shift.objects.filter(id_state__short_description='pendiente',
                                              date__gte=datetime.date.today()).order_by('hour')
    paginator = Paginator(pending_shifts, 5)
    return pending_shifts, paginator