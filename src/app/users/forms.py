from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User, UserProfile


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('active',)
        widgets = {
            'birthday': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}), 
        }
