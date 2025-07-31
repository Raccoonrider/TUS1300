from django.contrib import admin

from common.admin import ChainedPrepopulatedFieldsMixin
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

@admin.register(Control)
class ControlModelAdmin(ChainedPrepopulatedFieldsMixin, admin.ModelAdmin):
    model = Control
    list_display = ('name', 'event', 'distance', 'render_timedelta_close', 'render_datetime_close',)
    list_filter = ('event', )
    autocomplete_fields = ('event', )
    ordering = ('-event__date', 'distance')
    chained_prepopulated_fields = ('event',)

@admin.register(PaymentInfo)
class PaymentInfoModelAdmin(admin.ModelAdmin):
    model = PaymentInfo

@admin.register(SupportOrg)
class SupportOrgAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    model = SupportOrg
    search_fields = ('name', )
    list_display = ('name', 'brief')
    ordering = ('name',)

@admin.register(EventSupportOrg)
class EventSupportOrgModelAdmin(admin.ModelAdmin):
    model = EventSupportOrg
    list_display = ('support_org', 'event', 'priority')
    ordering = ('-event__date',)
    autocomplete_fields = ('support_org',)