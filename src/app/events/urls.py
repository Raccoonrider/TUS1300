from django.urls import include, path

from events.views import EventResults, EventDetail, ApplicationCreate, organizer_list

urlpatterns = [
    path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('<int:pk>/results/', EventResults.as_view(), name='event_results'),
    path('<int:pk>/org-tools/list/by_number/', organizer_list, kwargs={'order': 'number'}),
    path('<int:pk>/org-tools/list/by_name/', organizer_list, kwargs={'order': 'user_profile__last_name'}),
    path('<int:pk>/hx-payment-info/', EventDetail.hx_get_payment_info, name='hx_event_payment_info'),
    path('<int:pk>/application/create/', ApplicationCreate.as_view(), name="application_create"),
    path('hx-calendar/', EventDetail.hx_calendar, name='hx_calendar'),
    path('hx-results/', EventDetail.hx_results, name='hx_results'),

    ]