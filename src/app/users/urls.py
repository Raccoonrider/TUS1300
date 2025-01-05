from django.urls import include, path

from users.views import UserProfileCreateUpdate, user_redirect

urlpatterns = [
    path('create/', UserProfileCreateUpdate.as_view(), name="user_profile_create"),
    path('update/', UserProfileCreateUpdate.as_view(), name="user_profile_update"),
    path('logged_in/', user_redirect, name="user_redirect"),
    ]