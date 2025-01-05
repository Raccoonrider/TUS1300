from django.contrib import admin

from events.models import *

class BaseModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

@admin.register(Series)
class SeriesModelAdmin(BaseModelAdmin):
    model = Series
    search_fields = ('name',)
    list_display = ('__str__', 'active')
    list_filter = ('active', )
    ordering = ('-active', 'name')

@admin.register(Event)
class EventModelAdmin(BaseModelAdmin):
    model = Event
    search_fields = ('name',)
    list_display = ('__str__', 'date', 'time', 'series', 'finished', 'active')
    list_filter = ('active', 'series')
    ordering = ('-active', 'finished', '-date')
    autocomplete_fields = ('series',)


@admin.register(Route)
class RouteModelAdmin(BaseModelAdmin):
    model = Route
    search_fields = ('name', )
    list_display = ('__str__', 'series', 'active')
    list_filter = ('active',)
    ordering = ('-active', 'name')
    autocomplete_fields = ('series',)

@admin.register(Result)
class ResultModelAdmin(admin.ModelAdmin):
    model = Result
    search_fields = ('user_profile__last_name', 'user_profile__first_name')
    list_display = ('user_profile', 'number', 'render_category', 'time', 'status')
    list_filter = ('event', 'route', 'status')
    autocomplete_fields = ('event', 'route', 'user_profile')
    ordering = ('-event__date', 'status')


@admin.register(Application)
class ApplicationModelAdmin(admin.ModelAdmin):
    model = Application
    search_fields = ('user_profile__last_name', 'user_profile__first_name')
    list_display = ('user_profile', 'number', 'event', 'payment_confirmed', 'helmet_not_needed', 'route', 'category', 'created')
    autocomplete_fields = ('event', 'route', 'user_profile', 'result')
    list_filter = ('event', 'payment_confirmed', 'helmet_not_needed', 'route', 'category', 'referral')


@admin.register(EventRoute)
class EventRouteModelAdmin(admin.ModelAdmin):
    model = EventRoute
    list_display = ('__str__', 'event', 'route', 'active')
    list_filter = ('active', 'event')
    ordering = ('-active', '-event__date')
    autocomplete_fields = ('event', 'route',)

@admin.register(AgeGroup)
class AgeGroupModelAdmin(admin.ModelAdmin):
    model = AgeGroup
    list_display = ('event', 'gender', 'age_min', 'age_max')
    list_filter = ('event',)
    ordering = ('-event__date',)
    autocomplete_fields = ('event',)

@admin.register(PaymentWindow)
class PaymentWindowModelAdmin(admin.ModelAdmin):
    model = PaymentWindow
    list_display = ('event', 'price', 'active_until')
    list_filter = ('event',)
    ordering = ('-active_until',)
    autocomplete_fields = ('event',)

