import hashlib
import datetime
from django.core.mail import send_mail
from django.views.generic import View, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import Users
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm
from .helpers import generate_confirmation_code

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "user/home_user.html"
    login_url = reverse_lazy('user-login')


class UserRegisterView(FormView):
    template_name = 'user/register.html'
    
    form_class = UserRegisterForm
    success_url = '/register/'

    def form_valid(self, form):
        verification_code = generate_confirmation_code()
        user = Users.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['password'],
            picture=form.cleaned_data['picture'],
            start_time_attention=form.cleaned_data['start_time_attention'],
            end_time_attention=form.cleaned_data['end_time_attention'],
            code_verification=verification_code
        )
        date = datetime.datetime.now()
        date_str = date.strftime('%Y-%m-%d %H:%M:%S') 
        asunto = "Confirmacion de mail"
        message = "El codigo de verificacion es " \
                        + verification_code + \
                            " la hora es " + date_str
        email_remitente = "banckington@gmail.com"
         
        send_mail(asunto, message, email_remitente, ['iarzaesteban94@gmail.com',])
        return HttpResponseRedirect(
            reverse('user-verification',
                    kwargs={'pk': user.id})
        )
        # return super(UserRegisterView, self).form_valid(form)
    

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = "Usuario o contraseña incorrecta."
        try:
            user = Users.objects.filter(username=username).first()
            if user is not None and hashlib.sha256(password.encode()).hexdigest() == user.password:
                    user.loggin = True
                    user.save()
                    return redirect('home')
            else:
                messages.add_message(request=request, level=message.ERROR, message=message)

        except Users.DoesNotExist:
            messages.add_message(request=request, level=message.ERROR, message=message)

        return render(request, self.template_name, {'username': username})

class LoginUser(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/home-user/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            return super(LoginUser, self).form_valid(form)
        else:
            messages.error(self.request, "Usuario o contraseña incorrectos")
            return self.form_invalid(form)
    
class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)

        return HttpResponseRedirect(
            reverse('user-login')
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'user/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('user-login')
    login_url = reverse_lazy('user-login')
    
    def form_valid(self, form):
        current_user = self.request.user
        user = authenticate(username=current_user.username,
                            password=form.cleaned_data['current_password'])
        if user:
            new_password = form.cleaned_data['new_password']
            current_user.set_password(new_password)
            current_user.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
    
class CodeVerificationView(FormView):
    template_name = 'user/user_verification.html'
    form_class = VerificationForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
                        'pk': self.kwargs['pk']
        })
        return kwargs
    
    def form_valid(self, form):
        Users.objects.filter(id=self.kwargs['pk']).update(is_active=True)
        return super(CodeVerificationView, self).form_valid(form)


# class FechaMixin(object):

#     def get_context_data(self, **kwargs):
#         context = super(FechaMixin, self).get_context_data(**kwargs)
#         context["fecha"] = datetime.datetime.now()
#         return context
    

# class TemplatePruebaMixin(FechaMixin, TemplateView):
#     template_name = "user/mixin.html"