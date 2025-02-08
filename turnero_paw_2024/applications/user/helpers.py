import random
import string
from PIL import Image
from io import BytesIO

def generate_confirmation_code(length=15):
    characters = string.ascii_letters + string.digits
    confirmation_code = ''.join(random.choice(characters) for i in range(length))
    return confirmation_code

def process_picture(picture, user):
    img = Image.open(picture)
    try:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        output = BytesIO()
        img.save(output, format='JPEG', quality=70)
        user.picture = output.getvalue()
        output.close()
        
        user.save()
        return True
    except Exception as e:
        return False
     
def serialize_shifts(page_obj):
    return [{'date': shift.date, 
             'hour': shift.hour, 
             'id_person': str(shift.id_person),
             'operador': shift.id_person.id_user.username if shift.id_user else 'Sin Asignar',
             'state': shift.id_state.description} for shift in page_obj]