from django.urls import path
from . import views
from .views import LoginView, \
                        HomePage, \
                            UserRegisterView, \
                                LoginUser, \
                                    LogoutView, \
                                        UpdatePasswordView, \
                                            CodeVerificationView    
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('user-login/', LoginUser.as_view(), name='user-login'), 
    path('home-user/', HomePage.as_view(), name='home-user'), 
    path('user-logout/', LogoutView.as_view(), name='user-logout'), 
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'), 
    path('user-verification/<pk>/', CodeVerificationView.as_view(), name='user-verification'), 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)