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
from django.contrib.auth.decorators import login_required
from .models import Users
from applications.shift.models import Shift
from applications.aditional_information.models import AditionalInformation
from . import forms
from .helpers import generate_confirmation_code
from app.settings.base import EMAIL_HOST_USER
from applications.person.models import Person
from applications.state.models import State
from PIL import Image
from io import BytesIO

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
            if not user.has_default_password:
                return redirect('update-password')
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
        pending_shifts = Shift.objects.filter(id_state__short_description='pendiente',
                                              date__gte=datetime.date.today()).order_by('hour')
        paginator = Paginator(pending_shifts, 5)
        page = self.request.GET.get('page')
        try:
            pending_shifts = paginator.page(page)
        except PageNotAnInteger:
            pending_shifts = paginator.page(1)
        except EmptyPage:
            pending_shifts = paginator.page(paginator.num_pages)
        
        context['pending_shifts'] = pending_shifts
        return context

class UserRegisterView(FormView):
    template_name = 'user/register.html'
    form_class = forms.UserRegisterForm
    success_url = '/register/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            messages.error(self.request, 'El usuario ingresado ya está en uso')
            return super(UserRegisterView, self).form_valid(form)
        
        email = form.cleaned_data.get('email')
        if Person.objects.filter(email=email).exists():
            messages.error(self.request, 'Este correo electrónico ya está en uso')
            return super(UserRegisterView, self).form_valid(form)
        
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm_password')
        if password != confirm_password:
            messages.error(self.request, 'Las contraseñas no coinciden')
            return super(UserRegisterView, self).form_valid(form)
        
        verification_code = generate_confirmation_code()
        picture = form.cleaned_data.get('picture')
        output = BytesIO()
        if picture:
            img = Image.open(picture)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output, format='JPEG', quality=70)
        
        user = Users.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['password'],
            code_verification=verification_code,
            picture=output.getvalue()
        )

        user.save()
        
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
    success_url = '/home-user/'

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
                        'pk': self.kwargs['pk']
        })
        return kwargs
    
    def form_valid(self, form):
        Users.objects.filter(id=self.kwargs['pk']).update(is_active=True)
        return super(CodeVerificationView, self).form_valid(form)

class UpdateFooterView(LoginRequiredMixin, FormView):
    template_name = 'user/update_footer.html'    
    form_class = forms.UserUpdateFooterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aditional_information = AditionalInformation.objects.all()
        
        context['aditional_information'] = aditional_information
        return context
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            link = form.cleaned_data['link']
            icon_base64 = form.cleaned_data['icon_base64']            
            
            AditionalInformation.objects.create(
                title=title,
                description=description,
                link=link,
                icon=icon_base64
            )

            return JsonResponse({'success': True})
        
        return JsonResponse({'Error': True})
    
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'user/update_password.html'
    form_class = forms.UpdatePasswordForm
    success_url = '/update-password/'
    
    def form_valid(self, form):
        current_user = self.request.user
        new_password = form.cleaned_data['new_password']
        repeat_new_password = form.cleaned_data['repeat_new_password']
        if new_password != repeat_new_password:
            messages.error(self.request, 'Las contraseñas no coinciden')
            return super(UpdatePasswordView, self).form_valid(form)
            
        user = authenticate(username=current_user.username,
                            password=form.cleaned_data['current_password'])
        try:
            if user:
                current_user.set_password(new_password)
                if not current_user.has_default_password:
                    current_user.has_default_password = True
                current_user.save()
                logout(self.request)

                return HttpResponseRedirect(
                    reverse('user-login')
                )
            else:
                messages.error(self.request, 'La contraseña ingresada es incorrecta')
                return super(UpdatePasswordView, self).form_valid(form)
        except Exception as e:
            messages.error(self.request, 'Error al procesar el cambio de contraseña')
            return super(UpdatePasswordView, self).form_valid(form)
            


class UpdatePictureView(LoginRequiredMixin, FormView):
    template_name = 'user/update_picture.html'
    form_class = forms.UpdatePictureForm
    
    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['picture'] = user.picture
        return initial
    
    def form_valid(self, form):
        current_user = self.request.user
        picture = form.cleaned_data.get('picture')
        try:
            if picture:
                img = Image.open(picture)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                output = BytesIO()
                img.save(output, format='JPEG', quality=70)
                current_user.picture = output.getvalue()
                output.close()
                
            current_user.save()
            messages.success(self.request, 'La fotografía se ha actualizado correctamente.')
            return redirect('update-picture') 
        except Exception as e:
            messages.error(self.request, 'Por favor ingrese una imagen correcta')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al actualizar la fotografía. Por favor, inténtelo de nuevo.')
        return super().form_invalid(form)
    
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
             'operador': shift.id_person.id_user.username if shift.id_user else 'Sin Asignar',
             'state': shift.id_state.description} for shift in page_obj]

@login_required
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
    

class SendEmailView(LoginRequiredMixin, FormView):
    template_name = 'user/send_email.html'
    form_class = forms.SendEmailForm
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        
        try:
            send_mail(subject, message, EMAIL_HOST_USER, [email,])
            messages.success(self.request, f'Se ha enviado el correo electrónico a {email} correctamente.')
        except Exception as e:
            messages.error(self.request, f'Error al enviar el correo electrónico: {e}')
        
        return redirect('send-email')

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al enviar el correo electrónico. Por favor, inténtelo nuevamente.')
        return super().form_invalid(form)
    
@login_required
def update_attentions_times(request):
    current_user = request.user
    users = Users.objects.exclude(
                username=current_user.username
            ).exclude(
                start_time_attention__isnull=True
            ).exclude(
                end_time_attention__isnull=True
            )
            
    paginator = Paginator(users, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    return render(request, 'user/update_attentions_times.html', {'users': users})

@login_required
def get_confirm_shifts_today(request):
    today = datetime.datetime.now()
    list_shift = Shift.objects.filter(
                            id_state__short_description="confirmado",
                            date=today).order_by("hour")
    paginator = Paginator(list_shift, 5)
    page_number = request.GET.get("page")
    try:
        list_shift = paginator.page(page_number)
    except PageNotAnInteger:
        list_shift = paginator.page(1)
    except EmptyPage:
        list_shift = paginator.page(paginator.num_pages)

    return render(request, 'user/get_confirm_shifts_today.html', {'list_shift': list_shift})

@login_required
def view_user_shifts_today(request, username):
    # obtenemos todos los turnos confirmados para hoy del usuario seleccionado
    user_shifts_today = Shift.objects.filter(
                                id_user__username=username, 
                                id_state__short_description='confirmado',
                                date=datetime.date.today())
    
    paginator = Paginator(user_shifts_today, 5)
    page_number = request.GET.get("page")
    try:
        user_shifts_today = paginator.page(page_number)
    except PageNotAnInteger:
        user_shifts_today = paginator.page(1)
    except EmptyPage:
        user_shifts_today = paginator.page(paginator.num_pages)
    return render(request, 'user/user_shifts_today.html', {'user_shifts_today': user_shifts_today,
                                                           'username': username})

@login_required
def view_user_all_shifts(request, username):
    # Obtenemos los turnos confirmados por el usuario seleccionado 
    # del dia actial en adelante
    user_all_shifts = Shift.objects.filter(
                        id_user__username=username, 
                        id_state__short_description='confirmado',
                        date__gte=datetime.date.today())
    
    paginator = Paginator(user_all_shifts, 5)
    page_number = request.GET.get("page")
    try:
        user_all_shifts = paginator.page(page_number)
    except PageNotAnInteger:
        user_all_shifts = paginator.page(1)
    except EmptyPage:
        user_all_shifts = paginator.page(paginator.num_pages)
        
    return render(request, 'user/user_all_shifts.html', {'user_all_shifts': user_all_shifts,
                                                         'username': username})

@login_required
def export_to_excel(request):
    if request.method == 'GET':
        shifts = Shift.objects.filter(id_state__short_description='pendiente').order_by('date')
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte de Turnos"
        
        headers = ['Fecha', 'Hora', 'Persona', 'Operador Asignado', 'Estado']
        ws.append(headers)
        for shift in shifts:
            date_string = shift.date.strftime('%d-%m-%Y')
            row_data = [date_string, 
                        shift.hour, 
                        shift.id_person.last_name + " "+ shift.id_person.first_name, 
                        shift.id_person.id_user.username if shift.id_state.short_description == 'confirmado' else 'Sin Asignar',
                        shift.id_state.description]
            ws.append(row_data)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=reporte_turnos.xlsx'
        
        wb.save(response)
        
        return response
    else:
        return HttpResponse(status=405)

@login_required    
def get_user_avatar(request):
    user = request.user

    if user.picture:
        user.retrieve_image()
        return HttpResponse(user.picture, content_type='image/jpeg')
    else:
        return HttpResponse("El usuario no posee un avatar cargado")