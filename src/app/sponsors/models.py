import uuid
from datetime import date

from django.db import models
from django.contrib import admin
from django.apps import apps
from django.contrib.sites.shortcuts import get_current_site


from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseViewableModel, BaseRelation, BaseModel

class Sponsor(BaseViewableModel):
    xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка на сайт",
    )
    vk_xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка ВК",
    )
    phone_number = PhoneNumberField(
        null=True, 
        blank=True
    )
    image = models.ImageField(
        null=False,
        blank=False, 
        upload_to='sponsor_logo', 
        verbose_name="Лого",
        )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Профиль спонсора"
        verbose_name_plural = "Профили спонсоров"


class EventSponsor(BaseRelation):
    event = models.ForeignKey(
        to='events.Event',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Событие",
    )
    sponsor = models.ForeignKey(
        to='sponsors.Sponsor',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Спонсор",
    )

    class Meta:
        verbose_name = 'Связь "Спонсор-событие"'
        verbose_name_plural = 'Связь "Спонсор-событие"'



class Referral(BaseModel):
    code = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        verbose_name="Код",
        help_text="Код, который нужно указать при регистрации",
    )

    referral_uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        verbose_name="UUID",
        help_text="Код, который используется в реферальной ссылке",
    )

    discount = models.IntegerField(
        default=0,
        verbose_name="Скидка",
    )

    event = models.ForeignKey(
        to='events.Event', 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Событие",
        )

    expires = models.DateField(
        null=True,
        blank=True,
        verbose_name="Срок действия",
        help_text="Если не указывать - бессрочно",
    )

    sponsor = models.ForeignKey(
        to=Sponsor, 
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Спонсор",
    )

    class Meta:
        verbose_name = "Рефералка"
        verbose_name_plural = "Рефералки"

    @admin.display(description="Использований при оплате")
    def times_used(self):
        Application = apps.get_model(app_label='events', model_name='Application')

        q = Application.objects.filter(
            referral=self, 
            payment_confirmed=True
            )
        return len(q)
    
    @admin.display(description="Ссылка")
    def get_absolute_url(self):
        return f"https://xcm55.ru?ref_uuid={self.referral_uuid}"

    def __str__(self):
        return f"Рефералка {self.sponsor} на {self.event}"
    
    @classmethod
    def from_uuid(cls, value):
        return (
            cls.objects.filter(referral_uuid=value, active=True, expires__gte=date.today()).first()
            or cls.objects.filter(referral_uuid=value, active=True, expires__isnull=True).first()
        )