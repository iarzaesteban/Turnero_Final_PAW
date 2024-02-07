from django.urls import path
from . import views

urlpatterns = [
    path('aditional-information/', views.IndexView.as_view()),
]