from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.IndexView.as_view()),
]