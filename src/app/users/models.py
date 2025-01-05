from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel
from common.enums import Gender


class UserProfile(BaseModel):
    first_name = models.CharField(
        null=False, 
        blank=False, 
        max_length=255, 
        verbose_name="Имя",
    )
    last_name = models.CharField(
        null=False, 
        blank=False, 
        max_length=255, 
        verbose_name="Фамилия",
    )
    gender = models.IntegerField(
        null=False,
        blank=False,
        default=Gender.M,
        choices=Gender.choices(),
        verbose_name="Пол",
    )
    phone_number = PhoneNumberField(
        null=False,
        blank=False,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона для связи с организаторами",
    )
    birthday = models.DateField(
        null=False,
        blank=False,
        verbose_name="Дата рождения",
        help_text="Укажите точную дату рождения для определения "
        "возрастной категории на момент старта. " 
        "Ваша дата рождения будет скрыта от других пользователей "
        "и не отобразится на странице результатов ",
    )
    location = models.CharField(
        blank=True, 
        max_length=255, 
        verbose_name="Локация",
        help_text="Откуда Вы?"
    )
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_update_url(self):
        return reverse("user_profile_update")
    
    def get_createa_url(self):
        return reverse("user_profile_create")

    def age(self, date_:date|None=None):
        date_ = date_ or date.today()
        age = date_.year - self.birthday.year

        date_ = date_.replace(year=self.birthday.year)
        if date_ < self.birthday:
            age -= 1
        return age

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
    


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    profile = models.ForeignKey(
        to=UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
    
    def get_display_name(self):
        if self.profile:
            return F"{self.profile.last_name} {self.profile.first_name}"
        else:
            return self.email
            
    
    class Meta(AbstractBaseUser.Meta):
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'