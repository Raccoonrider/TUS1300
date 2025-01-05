from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from common.enums import Category
from events.models import Event, Route, EventRoute, Application


class ApplicationForm(forms.Form):
    route=forms.ModelChoiceField(
        queryset=Route.objects.all(),
        required=True,
        label="Дистанция",
        initial=1,
    )

    category=forms.ChoiceField(
        choices=(
            (Category.Default, 'Категория "Любители"'),
            (Category.Elite, 'Категория "Элита"')
        ),
        required=True,
        label="С кем я буду соревноваться",
        initial=Category.Default,
    )

    helmet_not_needed = forms.BooleanField(
        initial=True,
        required=False,
        label="Буду в своём шлеме",
        help_text="Если у Вас нет своего шлема, его можно будет взять напрокат на старте. Снимите эту галочку, чтобы мы знали, что он Вам понадобится."
    )

    confirm_rules=forms.BooleanField(
        initial=False,
        required=True,
        label=f"Ознакомлен с положением и правилами мероприятия"
    )

    confirm_personal=forms.BooleanField(
        initial=False,
        required=True,
        label=f"Согласен на обработку персональных данных"
    )



