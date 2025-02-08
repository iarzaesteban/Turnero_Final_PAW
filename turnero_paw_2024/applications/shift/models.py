import datetime
from django.core.paginator import Paginator
from django.db import models
from applications.person.models import Person
from applications.user.models import Users
from applications.state.models import State
from .constants import PENDING_SHIFT, CONFIRM_SHIFT

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


    def get_pending_shifts(order_by):
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