from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    id_user = models.ForeignKey('user.Users', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    

    def person_exists(email):
        return Person.objects.filter(email=email).exists()
    
    
    def create_person(person_data):
        return Person.objects.create(**person_data)
    
    def get_person(email):
        return Person.objects.get(email=email)
    
    def get_person_by_id_user(id_user):
        return Person.objects.get(id_user=id_user)

    def get_first_person(email):
        return Person.objects.filter(email=email).first()