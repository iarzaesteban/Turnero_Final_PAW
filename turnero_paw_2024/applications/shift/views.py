
import re
import json
import random
from datetime import datetime, timedelta

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import helpers
from .forms import CancelShiftForm
from applications.shift.models import Shift
from applications.state.models import State
from applications.person.models import Person
from app.settings.base import EMAIL_HOST_USER
from .constants import CONFIRM_SHIFT


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(TemplateView):
    template_name = 'shift/index.html'


@csrf_exempt
def get_list_dates(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_date = data.get('date')
        events = helpers.get_google_calendar_events(selected_date)

        return JsonResponse({'events': events})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def confirm_shift(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        first_name = data.get('name')
        last_name = data.get('last_name')
        selected_date_time = data.get('dateTime')
        # Verificamos que el cliente no tenga más de 2 turnos solicitados en estado pendiente
        if Shift.count_pending_shifts(email) >= 2:
            return JsonResponse({
                    'response': "error", 
                    "message": "La persona ya tiene más de 1 turno en estado pendiente"} )
        
        if not Person.person_exists(email):
            person = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
            Person.create_person(person)
        confirmation_code = helpers.generate_confirmation_code()
        cancelation_url = request.build_absolute_uri(reverse('cancel_shift')) + f'?confirmation_code={confirmation_code}'
        shift = Shift.create_shift(selected_date_time, email, confirmation_code, cancelation_url)
        event_data = {
            'shift_id': shift.id,
            'person_name': f"{shift.id_person.last_name} {shift.id_person.first_name}"
        }
        event_summary = json.dumps(event_data)
        event_description = f"Fecha: {shift.date}, Hora: {shift.hour}"
        shift_date = datetime.strptime(shift.date, '%Y-%m-%d').date()
        shift_time = datetime.strptime(shift.hour+":00", '%H:%M:%S').time()
        
        start_datetime = datetime.combine(shift_date, shift_time)
        end_datetime = start_datetime + timedelta(minutes=30)

        helpers.add_event_to_google_calendar(event_summary, event_description, start_datetime, end_datetime)
        obj_date = datetime.strptime(shift.date, '%Y-%m-%d')
        format_date = obj_date.strftime('%d/%m/%Y')
        shift_data = {
            'day': format_date,
            'hour': shift.hour,
            'person': shift.id_person.last_name +" "+ shift.id_person.first_name,
        }
        return JsonResponse({'response': "ok", "shift": shift_data})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def cancel_shift(request):
    if request.method == 'GET':
        confirmation_code = request.GET.get('confirmation_code')
        shift = get_object_or_404(Shift, confirmation_code=confirmation_code)
        return render(request, 'shift/shift_details_before_cancel.html', {'shift': shift})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def initiate_cancel_shift(request):
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')
        shift = get_object_or_404(Shift, confirmation_code=confirmation_code)
        helpers.send_confirmation_code(shift)
        return JsonResponse({'success': True, 'shift_id': shift.id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def confirm_cancel_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        form = CancelShiftForm(request.POST)

        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')
            cancel_description = form.cleaned_data.get('cancel_description')

            if Shift.is_shift_canceled(shift=shift):
                if verification_code:
                    if shift.verification_code == verification_code:
                        shift = Shift.cancel_shift(shift=shift)
                        return render(request, 'shift/confirm_cancel.html', {
                            'success_message': 'Se ha cancelado el turno de forma exitosa.',
                            'set_description': False,
                            'shift': shift,
                            'form': form
                        })
                    else:
                        return render(request, 'shift/confirm_cancel.html', {
                            'error': 'Código incorrecto',
                            'set_description': False,
                            'shift': shift,
                            'form': form
                        })

                if cancel_description:
                    if not re.match(r'^[a-zA-Z0-9\s.,/!?áéíóúÁÉÍÓÚñÑüÜ]+$', cancel_description):
                        return render(request, 'shift/confirm_cancel.html', {
                            'success_message': 'Se ha cancelado el turno de forma exitosa.',
                            'error': 'La descripción contiene caracteres no permitidos.',
                            'set_description': False,
                            'shift': shift,
                            'form': form
                        })
                    shift = Shift.add_shift_description(shift=shift, cancel_description=cancel_description)
                    return render(request, 'shift/confirm_cancel.html', {
                        'success_message': 'Se ha agregado la descripción al turno de forma exitosa.', 
                        'shift': shift,
                        'set_description': True,
                        'form': form
                    })

                if not cancel_description:
                    return render(request, 'shift/confirm_cancel.html', {
                        'success_message': 'Se ha cancelado el turno de forma exitosa.',
                        'set_description': True,
                        'shift': shift,
                        'form': form
                    })
            else:
                return render(request, 'shift/shift_details_before_cancel.html', {'shift': shift})

    else:
        form = CancelShiftForm()
    if Shift.is_shift_canceled(shift=shift):
        return render(request, 'shift/confirm_cancel.html', {'shift': shift, 'form': form})
    else:
        return render(request, 'shift/shift_details_before_cancel.html', {'shift': shift})

    
@login_required
def get_shifts_today(request):
    state = request.GET.get('state')
    title = f"Turnos {state}s para hoy"
    today = datetime.now()
    list_shift = {}
    list_shift = Shift.get_today_shifts(state=state, today=today, request=request)
    
    paginator = Shift.make_pagination(data=list_shift, number_rows=5)
    page_number = request.GET.get("page")
    try:
        list_shift = paginator.page(page_number)
    except PageNotAnInteger:
        list_shift = paginator.page(1)
    except EmptyPage:
        list_shift = paginator.page(paginator.num_pages)
    return render(request, 'user/today_shifts_states.html', {'list_shift': list_shift, 
                                                             'title': title,
                                                             'state': state})

class ConfirmShiftView(LoginRequiredMixin, View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        user = self.request.user
        try:
            return redirect(Shift.update_id_user_shift(shift=shift, user=user))
        
        except Exception as e:
            pending_shifts = Shift.get_pending_shifts()
            error_message = str(e)
            return render(request, 'user/home_user.html', {'pending_shifts': pending_shifts, 
                                                           'error_message': error_message})

class CancelShiftView(View):
    def post(self, request, shift_id):
        data = json.loads(request.body)
        description = data.get('description', '')
        shift = Shift.get_shift(id=shift_id)
        try:
            redirect_url = Shift.update_cancel_shift(shift=shift, description=description, method="POST")
            return JsonResponse({'redirect_url': redirect_url})
            
        except State.DoesNotExist:
            error_message = 'Estado de turno no encontrado'
            return JsonResponse({'error_message': error_message}, status=400)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'error_message': error_message}, status=500)

    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        
        try:
            return redirect(Shift.update_cancel_shift(shift=shift, 
                                                      method="GET",
                                                      operator_user=self.request.user))
        
        except Exception as e:
            if not isinstance(self.request.user, AnonymousUser):
                pending_shifts = Shift.get_pending_shifts()
                error_message = str(e)
                return render(request, 'user/home_user.html', {'pending_shifts': pending_shifts, 'error_message': error_message})
            return redirect('/shift/home/')
        

class CompleteShiftView(LoginRequiredMixin, View):
    def get(self, request, shift_id):
        shift = get_object_or_404(Shift, id=shift_id)
        try:
            now = timezone.now()
            shift_datetime = timezone.make_aware(datetime.combine(shift.date, shift.hour))
            if shift_datetime > now:
                error_message = 'No puedes completar un turno que aún no ha ocurrido.'
                if not isinstance(self.request.user, AnonymousUser):
                    list_shift = Shift.get_confirm_shifts()
                    return render(request, 'user/home_user.html', {
                                                    'list_shift': list_shift, 
                                                    'error_message': error_message})
            
            return redirect(Shift.update_shift_completed(shift=shift, user=self.request.user))
        
        except Exception as e:
            if not isinstance(self.request.user, AnonymousUser):
                list_shift = Shift.get_confirm_shifts()
                error_message = str(e)
                return render(request, 'user/home_user.html', {
                                                        'list_shift': list_shift, 
                                                        'error_message': error_message})
            return redirect('get-confirm-shifts-today')
        

class SearchShiftsView(View):
    def get(self, request):
        search_value = request.GET.get('search_value', '')
        shift = None
        turno_detalle = Shift.get_details_shift(search_value=search_value)
        
        if shift:
            turno_detalle = {
                'date': shift.date,
                'hour': shift.hour,
                'first_name': shift.id_person.first_name,
                'last_name': shift.id_person.last_name,
                'state': shift.id_state.description,
                'email': shift.id_person.email,
            }
            return JsonResponse({'turno_detalle': turno_detalle})
        else:
            return JsonResponse({'error': 'No se encontró ningún turno con ese código de confirmación.'})
    