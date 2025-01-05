from django.urls import include, path

from pdf_generator.views import *

urlpatterns = [
    path('event/<int:event_pk>/numbers/', event_numbers, name='pdf_event_numbers'),
    path('event/<int:event_pk>/numbers/html/', event_numbers, name='pdf_event_numbers', kwargs={'format': 'html'}),
    ]