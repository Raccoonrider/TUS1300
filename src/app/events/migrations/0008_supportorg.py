# Generated by Django 5.1.4 on 2025-01-10 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_rename_payment_info_paymentinfo_card_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportOrg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('saved', models.DateTimeField(auto_now=True, verbose_name='Дата сохранения')),
                ('active', models.BooleanField(default=True, verbose_name='Активен')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(blank=True)),
                ('brief', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='img', verbose_name='Картинка')),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
    ]
