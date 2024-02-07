from django.urls import path
from . import views

urlpatterns = [
    path('persona/', views.IndexView.as_view()),
]