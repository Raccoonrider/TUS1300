from django.contrib import admin

from events.models import *

class BaseModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Event)
class EventModelAdmin(BaseModelAdmin):
    model = Event
    search_fields = ('name',)
    list_display = ('__str__', 'date', 'time', 'finished', 'active')
    list_filter = ('active',)
    ordering = ('-active', 'finished', '-date')


@admin.register(Result)
class ResultModelAdmin(admin.ModelAdmin):
    model = Result
    search_fields = ('user_profile__last_name', 'user_profile__first_name')
    list_display = ('user_profile', 'number', 'time', 'status')
    list_filter = ('event', 'status')
    autocomplete_fields = ('event', 'user_profile')
    ordering = ('-event__date', 'status')


@admin.register(Application)
class ApplicationModelAdmin(admin.ModelAdmin):
    model = Application
    search_fields = ('user_profile__last_name', 'user_profile__first_name')
    list_display = ('user_profile', 'event', 'payment_confirmed', 'created')
    autocomplete_fields = ('user_profile', 'result')
    list_filter = ('event',)

@admin.register(PaymentInfo)
class PaymentInfoModelAdmin(admin.ModelAdmin):
    model = PaymentInfo

