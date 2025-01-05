from django.contrib import admin

from sponsors.models import *
from events.models import Application

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    model = Sponsor
    search_fields = ('name', )
    list_display = ('name', 'phone_number', 'active')
    list_filter = ('active',)
    ordering = ('-active', 'name')

@admin.register(EventSponsor)
class EventSponsorModelAdmin(admin.ModelAdmin):
    model = EventSponsor
    list_display = ('__str__', 'event', 'sponsor', 'active')
    list_filter = ('active', 'event')
    ordering = ('-active', '-event__date')
    autocomplete_fields = ('sponsor',)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    model = Referral
    search_fields = ('code', 'referral_uuid', 'sponsor__name')
    readonly_fields = ('times_used', 'get_absolute_url')
    list_display = ('sponsor', 'event', 'code', 'expires', 'active', 'get_absolute_url')
    list_filter = ('active', 'event')
    ordering = ('-active', )
