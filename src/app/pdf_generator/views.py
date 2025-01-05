import os
import math
from itertools import cycle
from collections import namedtuple

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

import pdfkit

from common.enums import *
from events.models import Event, Application
from sponsors.models import EventSponsor, Sponsor
from users.models import UserProfile, User
from sponsors.models import Sponsor

pdfkit_options = {
    'encoding': 'utf-8',
    'page-size': 'A4', 
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
}

if os.name != "posix":
    pdfkt_config = pdfkit.configuration(wkhtmltopdf=os.environ.get('wkhtmltopdf'))
else:
    pdfkt_config = pdfkit.configuration()


def event_numbers(request, event_pk:int, format='pdf'):
    template = 'pdf_generator/number.html'
    
    
    event = get_object_or_404(Event, pk=event_pk)
    applications = Application.objects.filter(event=event, payment_confirmed=True).order_by('number')
    sponsors = EventSponsor.objects.filter(event=event).order_by('priority')


    

    context = {
        'host': request.build_absolute_uri().split('/pdf/')[0],
        'event': event,
        'applications': applications,
        'extra_numbers': [str(x) for x in range(300, 320)],
        'sponsors': sponsors,
        'pdfkit_page_size': 'А5',
        'pdfkit_orientation': 'Landscape',
    }

    if format == 'html':
        return render(
            request=request, 
            template_name=template, 
            context=context
        )
    
    if format == 'pdf':
        html = render_to_string(
            request=request, 
            template_name=template, 
            context=context
        )
        pdf = pdfkit.from_string(
            input=html, 
            options=pdfkit_options, 
            configuration=pdfkt_config
        )

        return HttpResponse(pdf, content_type="application/pdf")