# Generated by Django 5.1.4 on 2025-01-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_alter_eventsupportorg_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='garmin_connect_url',
            field=models.URLField(blank=True, verbose_name='Garmin Connect URL'),
        ),
    ]
