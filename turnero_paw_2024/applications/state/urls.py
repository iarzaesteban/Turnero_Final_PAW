from django.urls import path
from . import views

urlpatterns = [
    path('estados/', views.IndexView.as_view()),
]