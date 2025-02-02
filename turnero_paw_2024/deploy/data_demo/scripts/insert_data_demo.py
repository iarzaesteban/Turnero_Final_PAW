"""
Atributes in csv
first_name = models.CharField(max_length=50)
last_name = models.CharField(max_length=50)
email = models.EmailField()
id_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
Returns the inserts in table persons
"""
import os
import sys
import django
import pandas as pd
from django.contrib.auth.hashers import make_password

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.local")
django.setup()

from applications.person.models import Person
from applications.user.models import Users


users_csv_path = "deploy/data_demo/users.csv"
users_df = pd.read_csv(users_csv_path)

inserted_users = {}
users_df['password'] = users_df['password'].astype(str)

for _, row in users_df.iterrows():
    user = Users.objects.create_user(
        username=row["username"],
        password=(str(row["password"])),
        start_time_attention=row["start_time_attention"],
        end_time_attention=row["end_time_attention"],
        has_set_attention_times=True
    )
    inserted_users[row["email"]] = user.id
    user.is_active = True
    user.save()

print(f"Se insertaron {len(inserted_users)} usuarios.")


persons_csv_path = "deploy/data_demo/persons.csv"
persons_df = pd.read_csv(persons_csv_path)

for _, row in persons_df.iterrows():
    email = row["email"]
    id_user = inserted_users.get(email) 

    person = Person(
        first_name=row["first_name"],
        last_name=row["last_name"],
        email=email,
        id_user_id=id_user if id_user else None,
    )
    person.save()

print(f"Se insertaron {len(persons_df)} personas en la tabla Persons.")







