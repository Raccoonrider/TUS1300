from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.db.models import F

from common.enums import ResultStatus,Gender
from events.models import Event, Application, Result

class EventDetail(View):
    model = Event

    def get(self, *args, pk=None, **kwargs):
        if pk is not None:
            event = get_object_or_404(self.model, pk=pk)
        else:
            event = (self.model.objects
                .filter(active=True, finished=False)
                .order_by('date')
                .first()
                ) or (Event.objects
                    .filter(active=True, finished=True)
                    .order_by('-date')
                    .first()
                )
        if self.request.user.is_authenticated and self.request.user.profile:
            my_application = (Application.objects
                .filter(event=event, user_profile=self.request.user.profile)
                .first()
                )
        else:
            my_application = None

        self.request.session['ref_uuid'] = self.request.GET.get('ref_uuid')

        applications = Application.objects.filter(event=event).order_by('user_profile__last_name')

        registration_disabled = (
            my_application is not None
            or event.finished == True
            or event.registration_closed == True
        )

        context = {
            'event': event,
            'my_application': my_application,
            'applications': applications,
            'registration_disabled': registration_disabled,
        }
        return render(request=self.request, template_name=event.detail_template, context=context)
    
    @classmethod
    def hx_get_payment_info(cls, request, pk):
        if request.user.is_authenticated and request.user.profile:
            event = get_object_or_404(cls.model, pk=pk)
            my_application = (Application.objects
                .filter(event=event, user_profile=request.user.profile)
                .first()
                )
            
            context = {
                'event': event,
                'my_application': my_application,
            }
            return render(request=request, template_name=event.hx_payment_template, context=context)
        else:
            return HttpResponse("")
        
    @classmethod
    def hx_calendar(cls, request):
        events = Event.objects.filter(active=True, finished=False)
        for event in events:
            event.checkmark = (
                request.user.is_authenticated 
                and request.user.profile 
                and Application.objects.filter(
                    event__in=events, 
                    user_profile=request.user.profile,
                    payment_confirmed=True,
                    )
            )

        context = {
            'events': events
        }
        return render(request=request, template_name='hx-calendar.html', context=context)
       
    @classmethod
    def hx_results(cls, request):
        events = Event.objects.filter(active=True, finished=True)
        for event in events:
            event.checkmark = (
                request.user.is_authenticated 
                and request.user.profile 
                and Application.objects.filter(
                    event__in=events, 
                    user_profile=request.user.profile,
                    payment_confirmed=True,
                    )
            )

        context = {
            'events': events
        }
        return render(request=request, template_name='hx-results.html', context=context)

    @classmethod
    def create_application(cls, request, pk):
        request.session['redirect'] = request.path
        if request.user.is_authenticated == False:
            return HttpResponseRedirect(settings.LOGIN_URL)
        if request.user.profile is None:
            return HttpResponseRedirect(reverse('user_profile_create'))
        
        event = Event.objects.get(pk=pk)
        if event.registration_closed:
            return HttpResponseRedirect('/')

        application = Application.objects.filter(
            event=event, 
            user_profile=request.user.profile)
        if application:
            return HttpResponseRedirect('/#applications')
        
        application = Application()
        application.event = event
        application.user_profile = request.user.profile
        application.save()
        return HttpResponseRedirect('/#applications')