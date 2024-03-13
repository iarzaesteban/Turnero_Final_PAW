from django.urls import path
from . import views
 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.LoginUser.as_view(), name='user-login'), 
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('home-user/', views.HomePage.as_view(), name='home-user'), 
    path('update-atention-time/', views.UpdateAtentionTimePage.as_view(), name='update-atention-time'), 
    path('user-logout/', views.LogoutView.as_view(), name='user-logout'), 
    path('update-password/', views.UpdatePasswordView.as_view(), name='update-password'), 
    path('user-verification/<pk>/', views.CodeVerificationView.as_view(), name='user-verification'),
    path('set-attention-times/', views.UpdateAtentionTimePage.as_view(), name='set-attention-times'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)