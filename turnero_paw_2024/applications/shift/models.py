import datetime
from django.core.paginator import Paginator
from django.db import models
from django.contrib.auth.models import AnonymousUser

from applications.person.models import Person
from applications.user.models import Users
from applications.state.models import State
from .constants import PENDING_SHIFT, CONFIRM_SHIFT, CANCEL_SHIFT
from . import helpers
class Shift(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    id_state = models.ForeignKey(State, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=50)
    confirmation_url = models.URLField(max_length=255)
    verification_code = models.CharField(max_length=6, default='')
    last_updated = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=250, default='')

    def __str__(self):
        return f"{self.date} {self.hour} - {self.id_person}"
    

    def get_pending_shifts_paginate():
        pending_shifts = Shift.objects.filter(id_state__short_description=PENDING_SHIFT,
                                                date__gte=datetime.date.today()).order_by('date','hour')
        paginator = Paginator(pending_shifts, 5)
        return pending_shifts, paginator
    
    def get_shifts_user_confirm(username, only_today):
        if only_today:
            return Shift.objects.filter(
                                    id_user__username=username, 
                                    id_state__short_description=CONFIRM_SHIFT,
                                    date=datetime.date.today())


        return Shift.objects.filter(
                            id_user__username=username, 
                            id_state__short_description=CONFIRM_SHIFT,
                            date__gte=
                            datetime.date.today()).order_by('date', 'hour')


    def get_pending_shifts(order_by=None):
        if order_by is not None:
            return Shift.objects.filter(id_state__short_description=PENDING_SHIFT).order_by(*order_by)
        return Shift.objects.filter(id_state__short_description=PENDING_SHIFT)


    def get_confirms_shifts_today(date, order_by):
        return Shift.objects.filter(id_state__short_description=CONFIRM_SHIFT,
                                date=date).order_by(order_by)


    def make_pagination(data, number_rows):
        return Paginator(data, number_rows)
    
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
    
    def get_shift_state_range_dates(query_number, get_query_number_int, state=None,start_date=None, end_date=None):
        if query_number == 2 or get_query_number_int == 2:
            list_shifts =  Shift.objects.filter(id_state__short_description=state, date__range=[start_date, end_date]).order_by('date')
            query_number = 2
        elif query_number == 3 or get_query_number_int == 3:
            list_shifts =  Shift.objects.filter(date__range=[start_date, end_date]).order_by('date')
            query_number = 3
        elif query_number == 4 or get_query_number_int == 4:
            list_shifts =  Shift.objects.filter(id_state__short_description=state).order_by('date')
            query_number = 4

        return list_shifts, query_number
    

    def count_pending_shifts(email):
        pending_state_id = State.objects.filter(short_description="pendiente").values_list('id', flat=True).first()

        pending_shifts_count = Shift.objects.filter(id_person__email=email, id_state=pending_state_id).count()

        return pending_shifts_count

    
    def create_shift(selected_date_time, email, confirmation_code, cancelation_url):
        person_instance = Person.get_person(email=email)
        split_selected_date = selected_date_time.split()
        
        shift = Shift.objects.create(
            date=split_selected_date[0],
            hour=split_selected_date[1],
            id_person=person_instance,
            id_state=State.objects.get(short_description=PENDING_SHIFT),
            confirmation_code=confirmation_code,
            confirmation_url=cancelation_url
        )
        
        return shift
    
    
    def cancel_shift(shift):
        shift.id_state = State.get_cancel_shifts()
        shift.save()
        helpers.send_mail_to_receiver(shift.id_user, shift, False)
        helpers.remove_event_from_google_calendar(shift.date, shift.hour, shift.id)
        return shift
    
    
    def add_shift_description(shift, cancel_description):
        shift.description = cancel_description
        shift.save()


    def is_shift_canceled(shift):
        return shift.id_state.short_description != CANCEL_SHIFT
    

    def get_today_shifts(state, today, request):
        if state == CONFIRM_SHIFT:
            list_shift = Shift.objects.filter(
                                    date=today,
                                    id_user=request.user.id, 
                                    id_state__short_description=state).order_by("hour")
        else:
            list_shift = Shift.objects.filter(
                                    date=today,
                                    id_state__short_description=state).order_by("hour")
            
        return list_shift
    

    def update_id_user_shift(shift, user):
        if shift.id_user:
            if user != shift.id_user:
                shift.id_user = user
                shift.save()
                return 'home-user'
        confirmed_state = State.objects.get(short_description=CONFIRM_SHIFT)
        shift.id_state = confirmed_state
        shift.id_user = user
        shift.save()
        helpers.send_mail_to_receiver(user, shift, True)
        return 'home-user'
    

    def get_shift(id):
        return Shift.objects.filter(id=id).first() 
    

    def update_cancel_shift(shift, description=None, method=None, operator_user=None):
        if method == "POST":
            canceled_state = State.get_cancel_shifts()

            shift.id_state = canceled_state
            shift.description = description
            shift.save()
            helpers.remove_event_from_google_calendar(shift.date, shift.hour, shift.id)
            helpers.send_mail_to_receiver(shift.id_user, shift, False)
            return '/shift/home/'
        
        if method == "GET":
            canceled_state = State.get_cancel_shifts()
            shift.id_state = canceled_state
            helpers.remove_event_from_google_calendar(shift.date, shift.hour, shift.id)
            if not isinstance(operator_user, AnonymousUser):
                shift.id_user = operator_user
                shift.save()
                helpers.send_mail_to_receiver(operator_user, shift, True)
                return 'home-user'
            shift.save()
            person = Person.get_person_by_id_user(id_user=shift.id_user)
            helpers.send_mail_to_operator(person.email, shift)
            return '/shift/home/'
        

    def get_confirm_shifts():
        return Shift.objects.filter(id_state__short_description='confirmado')
    

    def get_shifts_by_search_value(id=None, confirmation_code=None):
        if id and not confirmation_code:
            return Shift.objects.filter(id_person=id).first()
        
        Shift.objects.filter(confirmation_code=confirmation_code).first()

    
    def get_details_shift(search_value):
        
        if helpers.is_mail(search_value):
            person = Person.get_first_person(email=search_value)
            if person:
                shift = Shift.get_shifts_by_search_value(id=person.id)
        else:
            shift = Shift.get_shifts_by_search_value(confirmation_code=search_value).first()

        return shift
    

    def update_shift_completed(shift, user):
        complete_state = State.get_complete_shifts()
        shift.id_state = complete_state
        if not isinstance(user, AnonymousUser):
            user = user
            shift.id_user = user
            shift.save()
        shift.save()
        
        return 'get-confirm-shifts-today'