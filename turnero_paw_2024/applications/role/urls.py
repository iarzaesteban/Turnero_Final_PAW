from django.urls import path
from . import views

urlpatterns = [
    path('roles/', views.IndexView.as_view()),
]