import random
import calendar
from datetime import datetime, timedelta
from applications.shift.models import Shift
from applications.person.models import Person
from applications.user.models import Users
from applications.user.helpers import generate_confirmation_code
from applications.state.models import State

def run():
    count_inserts = int(input("Ingrese la cantida de shifts a agregar: "))
    count_shifts_current_day = int(input("Ingrese la cantida de shifts a agregar para el día actual: "))

    all_users = Users.objects.all()
    start_times = [user.start_time_attention for user in all_users if user.start_time_attention]
    end_times = [user.end_time_attention for user in all_users if user.end_time_attention]

    #Obtenmos el inicio de horario de atención mínino y máximo
    earliest_start = min(start_times) if start_times else datetime.now().time()
    latest_end = max(end_times) if end_times else datetime.now().time()
    
    # Obtenemos el mes actual y el año actual
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    # Calculamos tres meses en adelante
    future_month = current_month + 3
    if future_month > 12:
        future_month -= 12
        current_year += 1

    # Generamos un mes aleatorio entre el mes actual y tres meses en adelante
    random_month = random.randint(current_month, future_month)

    # Calculamos la cantidad de días en el mes seleccionado
    days_in_month = calendar.monthrange(current_year, random_month)[1]

    for _ in range(count_shifts_current_day):
        id_user = random.choice(Users.objects.all())
        id_person = random.choice(Person.objects.all())
        id_state = random.choice(State.objects.all())

        date = datetime.now().date()
        random_minutes = random.randint(0, 1) * 30
    
        hour = datetime.now().time().replace(
            hour=random.randint(earliest_start.hour, latest_end.hour),
            minute=random_minutes,
            second=0
        )

        confirmation_code = generate_confirmation_code()
        cancellation_url = f'http://localhost:8000/cancel_shift?confirmation_code={confirmation_code}'

        shift_fields = {
            'date': date,
            'hour': hour,
            'id_person': id_person,
            'id_user': id_user,
            'id_state': id_state,
            'confirmation_code': confirmation_code,
            'confirmation_url': cancellation_url
        }

        shift = Shift.objects.create(**shift_fields)
        shift.save()

    for _ in range(count_inserts):

        random_day = random.randint(1, days_in_month)
        date = datetime(current_year, random_month, random_day)
        random_minutes = random.randint(0, 1) * 30
    
        hour = datetime.now().time().replace(
            hour=random.randint(earliest_start.hour, latest_end.hour),
            minute=random_minutes,
            second=0
        )

        id_user = random.choice(Users.objects.all())
        id_person = random.choice(Person.objects.all())
        id_state = random.choice(State.objects.all())

        confirmation_code = generate_confirmation_code()
        cancellation_url = f'http://localhost:8000/cancel_shift?confirmation_code={confirmation_code}'


        shift_fields = {
            'date': date,
            'hour': hour,
            'id_person': id_person,
            'id_user': id_user,
            'id_state': id_state,
            'confirmation_code': confirmation_code,
            'confirmation_url' : cancellation_url
        }

        shift = Shift.objects.create(**shift_fields)
        shift.save()

    print("Script finish success")
