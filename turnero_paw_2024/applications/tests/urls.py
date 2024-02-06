from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.IndexView.as_view()),
]