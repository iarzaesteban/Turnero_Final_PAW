from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('get_google_calendar_events/', views.get_list_dates, name='get_google_calendar_events'),

]