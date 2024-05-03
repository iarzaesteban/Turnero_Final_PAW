import json
from django.contrib.auth.hashers import make_password
from applications.user.models import Users
from applications.user.helpers import generate_confirmation_code

def run():
    with open('applications/user/fixtures/user.json') as json_file:
        users_data = json.load(json_file)
        for user_data in users_data:
            username = user_data['fields']['username']
            password = user_data['fields']['password']
            print("vamos a get los siguinetes atributos")
            start_time_attention = user_data['fields'].get('start_time_attention', '')
            end_time_attention = user_data['fields'].get('end_time_attention', '')
            has_set_attention_times = user_data['fields'].get('has_set_attention_times', False)
            has_default_password = user_data['fields'].get('has_default_password', False)
            print(f"username  -{username}-")
            print(f"password  -{password}-")

            hashed_password = make_password(password)
            verification_code = generate_confirmation_code()
            user_fields = {
                'username': username,
                'password': hashed_password,
                'code_verification': verification_code,
                'has_set_attention_times': has_set_attention_times,
                'has_default_password': has_default_password,
                'is_active': True
            }
            if start_time_attention:
                user_fields['start_time_attention'] = start_time_attention
            if end_time_attention:
                user_fields['end_time_attention'] = end_time_attention

            user = Users.objects.create(**user_fields)
            user.save() 

        print("Script finish success")
