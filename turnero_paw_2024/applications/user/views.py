import datetime
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, ListView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import Users
from applications.shift.models import Shift
from . import forms
from .helpers import generate_confirmation_code
from app.settings.base import EMAIL_HOST_USER
from applications.person.models import Person


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
        
        person = Person.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            id_user=user
        )
        date = datetime.datetime.now()
        date_str = date.strftime('%Y-%m-%d %H:%M:%S') 
        asunto = "Confirmacion de mail"
        message = "El codigo de verificacion es " \
                        + verification_code + \
                            " la hora es " + date_str
                            
        send_mail(asunto, message, EMAIL_HOST_USER, [person.email,])
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


class UpdateAttentionTimePage(LoginRequiredMixin, FormView):
    template_name = "user/attention_time_user.html"
    form_class = forms.UpdateAttentionTimeUserForm
    success_url = '/update-attention-time/'
    
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
        return super(UpdateAttentionTimePage, self).form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['start_time_attention'] = user.start_time_attention
        initial['end_time_attention'] = user.end_time_attention
        return initial
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar los horarios.')
        return super(UpdateAttentionTimePage, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateAttentionTimePage, self).get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context
    
class ReportViews(LoginRequiredMixin, ListView):
    template_name = "user/shift_reports.html"
    form_class = forms.ShiftFilterForm
    model = Shift
    paginate_by = 5

    def get_queryset(self):
        queryset = Shift.objects.filter(date=datetime.now().date(), id_state__short_description='pendiente')
        form = self.form_class(self.request.GET)
        
        if form.is_valid():
            state = form.cleaned_data.get('state')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            filtered_queryset = Shift.objects.all()
            
            if state:
                filtered_queryset = filtered_queryset.filter(id_state__short_description=state)

            if start_date:
                filtered_queryset = filtered_queryset.filter(date__gte=start_date)

            if end_date:
                end_date += timedelta(days=1)
                filtered_queryset = filtered_queryset.filter(date__lt=end_date)
            
            queryset = filtered_queryset
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            state = form.cleaned_data.get('state')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            filtered_queryset = Shift.objects.all()
            
            if state:
                filtered_queryset = filtered_queryset.filter(id_state__short_description=state)

            if start_date:
                filtered_queryset = filtered_queryset.filter(date__gte=start_date)

            if end_date:
                end_date += timedelta(days=1)
                filtered_queryset = filtered_queryset.filter(date__lt=end_date)
            paginator = Paginator(filtered_queryset, self.paginate_by)

            page = request.GET.get('page')
            try:
                filtered_queryset = paginator.page(page)
            except PageNotAnInteger:
                filtered_queryset = paginator.page(1)
            except EmptyPage:
                filtered_queryset = paginator.page(paginator.num_pages)

            
            return self.render_to_response(filtered_queryset)
        else:
            # Handle invalid form here
            # You may want to provide some feedback to the user
            return super().get(request, *args, **kwargs)
    
# class ReportViews(LoginRequiredMixin, ListView):
#     template_name = "user/shift_reports.html"
#     queryset = Shift.objects.all()
#     paginate_by = 5

#     def get_context_data(self, **kwargs):
#         context = super(ReportViews, self).get_context_data(**kwargs)
#         context['form'] = forms.ShiftFilterForm()
#         form = forms.ShiftFilterForm(self.request.GET)
#         context['object_list'] = Shift.objects.filter(date=datetime.now().date(), id_state__short_description='pendiente')

#         if form.is_valid():
#             print("FORM ES IS VALID ASDSADSA",flush=True)
#             state = form.cleaned_data.get('state')
#             start_date = form.cleaned_data.get('start_date')
#             end_date = form.cleaned_data.get('end_date')
#             filtered_queryset = Shift.objects.all()
#             if state:
#                 filtered_queryset = filtered_queryset.filter(id_state__short_description=state)

#             if start_date:
#                 filtered_queryset = filtered_queryset.filter(date__gte=start_date)

#             if end_date:
#                 end_date += timedelta(days=1)
#                 filtered_queryset = filtered_queryset.filter(date__lt=end_date)
            
#             context['object_list'] = filtered_queryset
        
#         return context
    
    
def update_attentions_times(request):
    current_user = request.user
    User = get_user_model()
    users = User.objects.exclude(username=current_user.username)
    return render(request, 'user/update_attentions_times.html', {'users': users})

def view_user_shifts_today(request, username):
    user_shifts_today = Shift.objects.filter(id_user__username=username, date=datetime.date.today())
    return render(request, 'user/user_shifts_today.html', {'user_shifts_today': user_shifts_today,
                                                           'username': username})

def view_user_all_shifts(request, username):
    user_all_shifts = Shift.objects.filter(id_user__username=username, id_state__short_description='confirmado')
    return render(request, 'user/user_all_shifts.html', {'user_all_shifts': user_all_shifts,
                                                         'username': username})