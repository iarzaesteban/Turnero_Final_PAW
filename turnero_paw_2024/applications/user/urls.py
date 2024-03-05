from django.urls import path
from . import views
from .views import LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('usuarios/', views.IndexView.as_view()),
    #path('login/', LoginView.as_view(), name='login'),
    #path('login/', views.login, name='login'),
    # path('create-user/', views.create_user, name='create-user'),
]