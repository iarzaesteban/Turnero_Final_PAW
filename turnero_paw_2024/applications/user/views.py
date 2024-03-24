import datetime
import json
from openpyxl import Workbook
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.generic import View, ListView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from .models import Users
from applications.shift.models import Shift
from . import forms
from .helpers import generate_confirmation_code
from app.settings.base import EMAIL_HOST_USER
from applications.person.models import Person
from applications.state.models import State


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
        
        if (user.start_time_attention == start_time and user.end_time_attention == end_time):
            messages.warning(self.request, 'Por favor seleccione un horario de inicio o fin de atención diferente.')
            return super(UpdateAttentionTimePage, self).form_valid(form)
        
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
      

def first_get(state, start_date, end_date):
    list_shifts= None
    query_number = 1
    if state and start_date and end_date:
        list_shifts = Shift.objects.filter(id_state__short_description=state, date__range=[start_date, end_date]).order_by('date')
        query_number = 2
    elif start_date and end_date and not state:
        list_shifts = Shift.objects.filter(date__range=[start_date, end_date]).order_by('date')
        query_number = 3
    elif state:
        list_shifts = Shift.objects.filter(id_state__short_description=state).order_by('date')
        query_number = 4
    
    return list_shifts, query_number

def serialize_shifts(page_obj):
    return [{'date': shift.date, 
             'hour': shift.hour, 
             'id_person': str(shift.id_person),
             'operador': shift.id_person.id_user.username if shift.id_state.short_description == 'confirmado' else 'Sin Asignar'} for shift in page_obj]
    
def list_shifts_filter_views(request):
    list_shifts = None
    states = State.objects.all()
    start_date = request.POST.get('start-date')
    state = request.POST.get('state')
    end_date = request.POST.get('end-date')
    
    get_query_number = request.POST.get('query', 1)
    get_query_number_get = request.GET.get('query')
    if get_query_number == 1 and get_query_number_get:
        get_query_number = get_query_number_get
        
    get_query_number_int = int(get_query_number) if get_query_number else None
    
    list_shifts, query_number = first_get(state, start_date, end_date)
    
    if(get_query_number_int != 1 or query_number != 1):
        if query_number == 2 or get_query_number_int == 2:
            list_shifts =  Shift.objects.filter(id_state__short_description=state, date__range=[start_date, end_date]).order_by('date')
            query_number = 2
        elif query_number == 3 or get_query_number_int == 3:
            list_shifts =  Shift.objects.filter(date__range=[start_date, end_date]).order_by('date')
            query_number = 3
        elif query_number == 4 or get_query_number_int == 4:
            list_shifts =  Shift.objects.filter(id_state__short_description=state).order_by('date')
            query_number = 4
        
        paginator = Paginator(list_shifts, 5)
        page_number = request.POST.get("page")
        page_obj = paginator.get_page(page_number)
        serialized_page = {
            'number': page_obj.number,
            'paginator': paginator.num_pages,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        }
        serialized_data = serialize_shifts(page_obj)
        
        return JsonResponse({'page_obj': serialized_page, 
                             'serialized_data': serialized_data, 
                             'query_number': query_number})

    else:
        list_shifts = Shift.objects.filter(id_state__short_description='pendiente').order_by('date')
        query_number = 1   
    
    paginator = Paginator(list_shifts, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "user/shifts_reports.html", {"page_obj": page_obj,
                                                             "list_shifts": list_shifts,
                                                             "states": states,
                                                             "query_number": query_number})
    
    
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
    
def export_to_excel(request):
    if request.method == 'GET':
        shifts = Shift.objects.filter(id_state__short_description='pendiente').order_by('date')
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte de Turnos"
        
        headers = ['Fecha', 'Hora', 'Persona', 'Operador Asignado']
        ws.append(headers)
        for shift in shifts:
            date_string = shift.date.strftime('%d-%m-%Y')
            row_data = [date_string, 
                        shift.hour, 
                        shift.id_person.last_name + " "+ shift.id_person.first_name, 
                        shift.id_person.id_user.username if shift.id_state.short_description == 'confirmado' else 'Sin Asignar']
            ws.append(row_data)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=reporte_turnos.xlsx'
        
        wb.save(response)
        
        return response
    else:
        return HttpResponse(status=405)