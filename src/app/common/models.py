from django.db import models

from common.shortcuts import transliterate


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    saved = models.DateTimeField(auto_now=True, verbose_name="Дата сохранения")
    active = models.BooleanField(null=False, default=True, verbose_name="Активен")

    class Meta:
        abstract = True


class BaseViewableModel(BaseModel):
    name = models.CharField(
        max_length=200, 
        verbose_name="Название",
        ) 
    slug = models.SlugField(
        blank=True,
        )
    brief = models.TextField(
        blank=True, 
        verbose_name='Краткое описание',
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание',
        )
    image = models.ImageField(
        null=True,
        upload_to='img', 
        blank=True, 
        verbose_name="Картинка",
        )
    
    class Meta:
        abstract = True

    def get_display_name(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    
class BaseRelation(BaseModel):
    """Basic model for Many-to-Many relationships"""
    priority = models.IntegerField(
        default=1,
        null=False,
        blank=True,
        verbose_name="Приоритет"
    )

    class Meta:
        abstract = True
        ordering = ('priority', 'pk')