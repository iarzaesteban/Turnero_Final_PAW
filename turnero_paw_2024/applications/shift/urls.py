from django.urls import include, path
from . import views


urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('get_google_calendar_events/', views.get_list_dates, name='get_google_calendar_events'),
    path('confirm_shift/', views.confirm_shift, name='confirm_shift'),
    path('cancel-shift/', views.cancel_shift, name='cancel_shift'),

]