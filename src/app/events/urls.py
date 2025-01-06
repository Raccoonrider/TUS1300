from django.urls import include, path

from events.views import EventDetail

urlpatterns = [
    path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('<int:pk>/hx-payment-info/', EventDetail.hx_get_payment_info, name='hx_event_payment_info'),
    path('<int:pk>/application/create/', EventDetail.create_application, name="application_create"),
    path('hx-calendar/', EventDetail.hx_calendar, name='hx_calendar'),
    path('hx-results/', EventDetail.hx_results, name='hx_results'),

    ]