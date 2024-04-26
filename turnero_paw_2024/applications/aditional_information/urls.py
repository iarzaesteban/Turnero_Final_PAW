from django.urls import path
from . import views

urlpatterns = [
    path('aditional-information/', 
         views.aditional_information_api, 
         name='aditional_information_api'),
    path('delete-aditional-information/<int:pk>/', 
         views.delete_aditional_information, 
         name='delete-aditional-information'),
    path('update-aditional-information/<int:pk>/', 
         views.update_aditional_information, 
         name='update-aditional-information'),
]