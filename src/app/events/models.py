from django.db import models
from django.urls import reverse
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from segno import make_qr

from common.models import BaseViewableModel, BaseModel
from common.enums import ResultStatus
from common.shortcuts import render_date


class Event(BaseViewableModel):
    distance = models.IntegerField(
        verbose_name="Дистанция",
        )
    map_embed_src = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Ссылка на карту",
        ) 
    gpx = models.FileField(
        upload_to="gpx", 
        blank=True, 
        verbose_name="Трек *.gpx",
        )

    date = models.DateField(
        null=False,
        verbose_name="Дата",
        )
    time = models.TimeField(
        null=True,
        verbose_name="Время старта",
    )
    start_location = models.CharField(
        null=True,
        verbose_name="Место старта",
        max_length=255,
    ) 
    vk_xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка ВК",
        )
    legend_doc = models.FileField(
        blank=True,
        verbose_name="Легенда",
        upload_to="event_rules"
    )
    rules_txt = models.TextField(
        blank=True,
        verbose_name="Коротко о правилах"
    )
    rules_url = models.URLField(
        blank=True,
        verbose_name="Ссылка на правила"
    )
    qualification_txt = models.TextField(
        blank=True,
        verbose_name="Коротко о квалификации"
    )
    support_txt = models.TextField(
        blank=True,
        verbose_name="Коротко о поддержке"
    )
    finished = models.BooleanField(
        default=False,
        verbose_name="Событие закончено",
    )
    registration_closed = models.BooleanField(
        default=False,
        verbose_name="Регистрация закрыта",
    )
    payment = models.ForeignKey('events.PaymentInfo', null=True, on_delete=models.SET_NULL)
    emegrency_phone_number = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name="Номер телефона для экстренной связи",
        help_text="Для печати на номерах",
    )
    result_qr = models.ImageField(
        null=True,
        blank=True,
        verbose_name="QR протокола",
        help_text="Для печати на номерах",
        upload_to='events/results_qr'
    )
    detail_template = models.CharField(
        null=False,
        blank=False,
        default='events/detail.html',
        max_length=127,
        verbose_name="Шаблон лэндинга",
    )
    results_template = models.CharField(
        null=False,
        blank=False,
        default='events/results.html',
        max_length=127,
        verbose_name="Шаблон протокола",
    )
    hx_payment_template = models.CharField(
        null=False,
        blank=False,
        default='events/hx_payment_info.html',
        max_length=127,
        verbose_name="Шаблон платежа",
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Cобытия"
    
    def get_display_name(self):
        return f"{self.name} - {self.date.year}"
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk':self.pk})
    
    def get_results_url(self):
        return reverse('event_results', kwargs={'pk':self.pk})
    
    def application_url(self):
        return reverse('application_create', kwargs={'pk':self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PaymentInfo(BaseModel):
    payment_value = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Сумма к оплате"
    )
    payment_info = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Номер карты",
    )
    payment_url = models.URLField(
        null=True,
        blank=True,
        verbose_name="URL для оплаты",
    )
    payment_qr = models.ImageField(
        null=True,
        blank=True,
        verbose_name="QR для оплаты",
        upload_to='events/payment_qr',
    )
    payment_sbp_phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name="Телефон для оплаты по СБП",   
    )
    payment_sbp_name = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        verbose_name="ФИО для оплаты по СБП",   
    )

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'

class Application(BaseModel):
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Событие",
    )
    user_profile = models.ForeignKey(
        to='users.UserProfile',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Профиль пользователя"
    )
    payment_confirmed = models.BooleanField(
        default=False,
        verbose_name="Оплата прошла"
    )
    result = models.ForeignKey(
        to='events.Result',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Результат"
    )
    number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Номер",
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"Заявка {self.user_profile.render_name()}"

class Result(BaseModel):
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Событие",
    )
    number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Номер"
    )
    user_profile = models.ForeignKey(
        to='users.UserProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Профиль пользователя"
    )
    time = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Время"
    )
    status = models.IntegerField(
        default=ResultStatus.OK,
        choices=ResultStatus.choices(),
        verbose_name="Статус",
    )
    
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def render_time(self):
        if self.time:
            t = round(self.time.total_seconds())
            h, t = divmod(t, 3600)
            m, s = divmod(t, 60)

            return F"{h:02d}:{m:02d}:{s:02d} {self.render_status()}" 
        return f"--:--:-- {self.render_status()}"
    
    def render_status(self):
        if self.status == ResultStatus.OK:
            return ""
        return ResultStatus.name_int(self.status)

    def avg_speed(self):
        if self.time:
            return "{:.02f} км/ч".format(self.event.distance / self.time.total_seconds() * 3600)
        return "-"

    def __str__(self):
        return F"{self.number} | {self.render_time()}"
