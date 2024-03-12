from django.urls import include, path
from . import views


urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('get_google_calendar_events/', views.get_list_dates, name='get_google_calendar_events'),
    path('confirm_shift/', views.confirm_shift, name='confirm_shift'),
    path('cancel-shift/', views.cancel_shift, name='cancel_shift'),
    path('confirmar-turno/<int:shift_id>/', views.ConfirmShiftView.as_view(), name='confirmar-turno'),
    path('cancelar-turno/<int:shift_id>/', views.CancelShiftView.as_view(), name='cancelar-turno'),
    path('buscar-turno/', views.BuscarTurnoView.as_view(), name='buscar-turno'),
]