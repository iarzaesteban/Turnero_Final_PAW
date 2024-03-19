from django.urls import path
from . import views
 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.LoginUser.as_view(), name='user-login'), 
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('home-user/', views.HomePage.as_view(), name='home-user'), 
    path('update-attention-time/', views.UpdateAttentionTimePage.as_view(), name='update-attention-time'),
    path('get-attenttions-times/', views.update_attentions_times, name='get-attentions-times'),
    path('user-logout/', views.LogoutView.as_view(), name='user-logout'), 
    path('update-password/', views.UpdatePasswordView.as_view(), name='update-password'), 
    path('user-verification/<pk>/', views.CodeVerificationView.as_view(), name='user-verification'),
    path('set-attention-times/', views.UpdateAttentionTimePage.as_view(), name='set-attention-times'),
    path('view-user-shifts-today/<username>/', views.view_user_shifts_today, name='view-user-shifts-today'),
    path('view-user-all-shifts/<username>/', views.view_user_all_shifts, name='view-user-all-shifts'),
    path('reports/', views.ReportViews.as_view(), name='reports'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)