from django.urls import include, path
from . import views
from .views import solicitud_turno

urlpatterns = [
    path('turnos/', views.IndexView.as_view()),
    path('solicitud-turno/', solicitud_turno, name='solicitud_turno'),

]
