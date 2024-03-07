from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from .models import Users

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware ejecutándose...")
        response = self.get_response(request)

        # Verifica si el usuario está autenticado
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_time = timezone.now()

            # Verifica si ha pasado el tiempo de inactividad
            if last_activity and (current_time - last_activity) > timedelta(minutes=1):
                # Cierra la sesión y actualiza el atributo 'loggin'
                user = Users.objects.get(username=request.user.username)
                user.loggin = False
                user.save()
                request.session.flush()

                # Redirige a la página de inicio de sesión
                return redirect('login')

            # Actualiza la hora de la última actividad
            request.session['last_activity'] = current_time

        return response
