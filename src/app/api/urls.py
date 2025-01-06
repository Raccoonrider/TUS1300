from django.urls import path, include

import api.views

urlpatterns = [
        path('events/', api.views.EventListAPIView.as_view()),
        path('events/<int:pk>/', api.views.EventDetailAPIView.as_view()),
        path('events/<int:event__pk>/applications/', api.views.ApplicationListAPIView.as_view()),
        path('events/<int:event__pk>/results/', api.views.ResultListCreateUpdateAPIView.as_view()),
        path('events/<int:event__pk>/results/', api.views.ResultListCreateUpdateAPIView.as_view()),
        path('events/results/add/', api.views.ResultListCreateUpdateAPIView.as_view()),
    ]   