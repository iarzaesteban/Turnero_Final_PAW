import hashlib
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from .models import Users
from .forms import LoginForm, CreateUserForm

# Create your views here.
class IndexView(TemplateView):
    template_name = '/user.html'


from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Users


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        message = "Usuario o contraseña incorrecta."
        try:
            user = Users.objects.filter(username=username).first()
            if user is not None:
                if hashlib.sha256(password.encode()).hexdigest() == user.password_hash:
                    return redirect('home')
                else:
                    messages.error(request, message)
            else:
                messages.error(request, message)

        except Users.DoesNotExist:
            messages.error(request, message)

        return render(request, self.template_name, {'username': username})
