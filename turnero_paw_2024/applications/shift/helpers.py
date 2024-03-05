import random
import string

from applications.person.models import Person
from applications.shift.models import Shift
from applications.state.models import State

def client_exists(email):
    print("EMAIL ES {}".format(email),flush=True)
    person = Person.objects.filter(email=email)
    print("person ES {}".format(person),flush=True)
    if person:
        return True
    return False

def create_client(email, first_name, last_name):
    Person.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

def create_shift(selected_date_time, email, confirmation_code, cancelation_url):
    person_instance = Person.objects.get(email=email)
    split_selected_date = selected_date_time.split()
    Shift.objects.create(
        date=split_selected_date[0],
        hour=split_selected_date[1],
        id_person=person_instance,
        id_state=State.objects.get(short_description="pendiente"),
        confirmation_code=confirmation_code,
        confirmation_url=cancelation_url
    )


def generate_confirmation_code(length=15):
    characters = string.ascii_letters + string.digits
    confirmation_code = ''.join(random.choice(characters) for i in range(length))
    return confirmation_code