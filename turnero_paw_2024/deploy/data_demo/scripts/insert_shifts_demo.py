import os
import sys
from collections import defaultdict
import django
from django.db.models import Min, Max, F, Count, Q
import random
from datetime import datetime, timedelta, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.local")
django.setup()

from applications.person.models import Person
from applications.user.models import Users
from applications.state.models import State
from applications.shift.models import Shift
from applications.shift.helpers import generate_confirmation_code

states = State.objects.all()

shifts = {}
cancelation_url = 'http://localhost:8000/shift/cancel-shift/'
# Definir el número máximo de turnos pendientes permitidos por usuario
MAX_PENDING_SHIFTS_PER_USER = 2
PENDING_SHIFT = 'Pendiente'
# Lista de correos electrónicos válidos
valid_emails = [
    'juancarlosiarza@gmail.com',
    'iarzaesteban94@gmail.com',
    'esteban_sanjo@hotmail.com',
    'banckington@gmail.com',
    'noeliabio120692@gmail.com'
]
# Posibles causas de cancelación de un turno
cancellation_reasons = [
        "El cliente no se presentó.",
        "Problemas de salud.",
        "Conflictos de agenda.",
        "He encontrado otro proveedor.",
        "El operador no está disponible.",
        "Problemas técnicos en el lugar.",
        "Condiciones climáticas adversas.",
        "Error en la programación de la cita.",
        "El servicio solicitado ya no es necesario.",
        ""
    ]

# Filtrar personas con los correos electrónicos válidos
persons_valid_email = Person.objects.filter(email__in=valid_emails)

def calculate_available_pending_shifts():   
    # Inicializar un diccionario para almacenar los espacios de turno pendientes disponibles por usuario
    available_shifts_count = 0
    # Recuperar usuarios con tiempos de atención definidos
    users_with_attention_times = Users.objects.filter(
        start_time_attention__isnull=False,
        end_time_attention__isnull=False
    )
    for user in users_with_attention_times:
        available_shifts_count += MAX_PENDING_SHIFTS_PER_USER

    return available_shifts_count


def generate_random_day():
    """
    Genera una fecha aleatoria entre la fecha actual y tres meses en el futuro.
    """
    today = datetime.today()
    three_months_later = today + timedelta(days=90)
    random_day = today + (three_months_later - today) * random.random()
    return random_day.date()


def generate_random_hour():
    """
    Genera una hora aleatoria entre dos horas dadas.
    """
    # Obtener usuarios con horarios de atención definidos
    users = Users.objects.filter(
        start_time_attention__isnull=False,
        end_time_attention__isnull=False
    ).annotate(
        start_time=F('start_time_attention'),
        end_time=F('end_time_attention')
    )

    if not users.exists():
        raise ValueError("No hay usuarios con horarios de atención definidos.")

    # Crear un diccionario para contar los turnos pendientes por horario
    pending_shifts_count = defaultdict(int)
    # Calcular los intervalos de atención disponibles y contar turnos pendientes
    for user in users:
        today = datetime.combine(datetime.today(), time.min)
        start_datetime = datetime.combine(today, user.start_time)
        end_datetime = datetime.combine(today, user.end_time)
        current_datetime = start_datetime
        while current_datetime <= end_datetime - timedelta(minutes=30):
            current_time = current_datetime.time()
            pending_shifts_count[current_time] += Shift.objects.filter(
                date=datetime.today(),
                hour=current_time,
                id_state__short_description='pendiente'
            ).count()
            current_datetime += timedelta(minutes=30)

    # Filtrar horarios con disponibilidad para nuevos turnos pendientes
    available_times = [
        time for time, count in pending_shifts_count.items()
        if count < users.count() * 2
    ]

    if not available_times:
        raise ValueError("No hay horarios disponibles para nuevos turnos pendientes.")

    # Seleccionar aleatoriamente una hora disponible
    selected_time = random.choice(available_times)

    return selected_time


def get_person_by_shift_state(shift_state):
    # Filtrar personas con los correos electrónicos válidos
    persons = persons_valid_email 
    if shift_state == PENDING_SHIFT:
        # Anotar la cantidad de turnos en estado 'pendiente' que tiene cada persona
        persons = persons.annotate(
            pending_shifts_count=Count('shift', filter=Q(shift__id_state_id__description=PENDING_SHIFT))
        ).filter(pending_shifts_count__lt=2)
    # Obtener la primera persona que cumple con los criterios
    person = persons.first()

    if not person:
        raise ValueError("No se encontró una persona que cumpla con los criterios especificados.")

    return person


def get_random_user():
     # Filtrar usuarios que tienen 'start_time_attention' y 'end_time_attention' no nulos
    users_with_attention_times = Users.objects.filter(
        start_time_attention__isnull=False,
        end_time_attention__isnull=False
    )
    # Obtener el número total de usuarios
    count = users_with_attention_times.count()
    if count == 0:
        raise ValueError("No hay usuarios disponibles.")
    # Generar un índice aleatorio
    random_index = random.randint(0, count - 1)
    # Obtener el usuario en la posición del índice aleatorio
    random_user = users_with_attention_times[random_index]
    return random_user

def get_random_cancellation_reason():
    return random.choice(cancellation_reasons)

for state in states:
    while True:
        try:
            if state.description == PENDING_SHIFT:
                #Solo 2 turnos pendiende por cliente
                available_shifts = calculate_available_pending_shifts()
                prompt = f"¿Cuántos turnos '{state.description}' deseas ingresar? Disponibles: {available_shifts}. "
            else:
                prompt = f"¿Cuántos turnos '{state.description}' deseas ingresar? "

            count = int(input(prompt))
            if count < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            shifts[state.description] = count
            break
        except ValueError as e:
            print(f"Error: {e}. Por favor, ingresa un número entero positivo.")

for state in states:    
    
    for i in range(shifts[state.description]):
        user = None
        description = ""
        confirmation_code = generate_confirmation_code()
        cancel_url = cancelation_url + f'?confirmation_code={confirmation_code}'
        
        #Si no es un estado pendiente seleccionar cualquier usuario que este activo con horarios de atención seteados
        person = get_person_by_shift_state(state.description)
        if state.description != PENDING_SHIFT:
            user = get_random_user()

        if state.description == "Cancelado":
            description = get_random_cancellation_reason()

        shift = Shift.objects.create(
            date=generate_random_day(),
            hour=generate_random_hour(),
            confirmation_code=confirmation_code,
            confirmation_url=cancel_url,
            id_person=person,
            id_state=state,
            id_user=user,
            description=description
        )
        shift.save()

print(f"Se han insertado {sum(shifts.values())} turnos en total.")
