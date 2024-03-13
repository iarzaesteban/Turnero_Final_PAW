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
from applications.shift.models import Shift
from . import forms
from .helpers import generate_confirmation_code
from app.settings.base import EMAIL_HOST_USER



class LoginUser(FormView):
    template_name = 'login.html'
    form_class = forms.LoginForm
    success_url = '/home-user/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            if not user.has_set_attention_times:
                return redirect('set-attention-times')
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
        
class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "user/home_user.html"
    login_url = reverse_lazy('user-login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pending_shifts = Shift.objects.filter(id_state__short_description='pendiente')
        context['pending_shifts'] = pending_shifts
        return context

class UserRegisterView(FormView):
    template_name = 'user/register.html'
    form_class = forms.UserRegisterForm
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
        print("EMAIL_HOST_USER to send {}".format(EMAIL_HOST_USER),flush=True)
        send_mail(asunto, message, EMAIL_HOST_USER, ['iarzaesteban94@gmail.com',])
        return HttpResponseRedirect(
            reverse('user-verification',
                    kwargs={'pk': user.id})
        )

class CodeVerificationView(FormView):
    template_name = 'user/user_verification.html'
    form_class = forms.VerificationForm
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
    
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'user/update_password.html'
    form_class = forms.UpdatePasswordForm
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


class UpdateAtentionTimePage(LoginRequiredMixin, FormView):
    template_name = "user/atention_time_user.html"
    form_class = forms.UpdateAtentionTimeUserForm
    success_url = '/update-atention-time/'
    
    def form_valid(self, form):
        start_time = form.cleaned_data['start_time_attention']
        end_time = form.cleaned_data['end_time_attention']
        
        user = self.request.user
        if not user.has_set_attention_times:
            user.has_set_attention_times = True
            user.start_time_attention = start_time
            user.end_time_attention = end_time
            user.save()
            return redirect('home-user')
        user.start_time_attention = start_time
        user.end_time_attention = end_time
        user.save()

        messages.success(self.request, 'Horarios actualizados correctamente.')
        return super(UpdateAtentionTimePage, self).form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['start_time_attention'] = user.start_time_attention
        initial['end_time_attention'] = user.end_time_attention
        return initial
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar los horarios.')
        return super(UpdateAtentionTimePage, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateAtentionTimePage, self).get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context
    
    # def form_valid(self, form):
    #     current_user = self.request.user
    #     user = authenticate(username=current_user.username,
    #                         password=form.cleaned_data['current_password'])
    #     if user:
    #         new_password = form.cleaned_data['new_password']
    #         current_user.set_password(new_password)
    #         current_user.save()

    #     logout(self.request)
    #     return super(UpdateAtentionTimePage, self).form_valid(form)

        
# class FechaMixin(object):

#     def get_context_data(self, **kwargs):
#         context = super(FechaMixin, self).get_context_data(**kwargs)
#         context["fecha"] = datetime.datetime.now()
#         return context
    

# class TemplatePruebaMixin(FechaMixin, TemplateView):
#     template_name = "user/mixin.html"