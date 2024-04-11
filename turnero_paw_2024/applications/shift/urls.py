from django.urls import include, path
from . import views


urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('get_google_calendar_events/', views.get_list_dates, name='get_google_calendar_events'),
    path('confirm_shift/', views.confirm_shift, name='confirm_shift'),
    path('cancel-shift/', views.cancel_shift, name='cancel_shift'),
    path('get-shifts-today/', views.get_shifts_today, name='get_shifts_today'),
    path('user-confirm-shift/<int:shift_id>/', views.ConfirmShiftView.as_view(), name='user-confirm-shift'),
    path('user-cancel-shift/<int:shift_id>/', views.CancelShiftView.as_view(), name='user-cancel-shift'),
    path('user-complete-shift/<int:shift_id>/', views.CompleteShiftView.as_view(), name='user-complete-shift'),
    path('search-shift/', views.SearchShiftsView.as_view(), name='search-shift'),
]