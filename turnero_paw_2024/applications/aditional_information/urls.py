from django.urls import path
from . import views

urlpatterns = [
    path('aditional-information/', 
         views.aditional_information_api, 
         name='aditional_information_api'),
]