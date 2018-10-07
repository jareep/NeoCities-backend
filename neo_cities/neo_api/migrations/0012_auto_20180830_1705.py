# Generated by Django 2.0 on 2018-08-30 17:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('neo_api', '0011_auto_20180716_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='difficulty',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='failure_message',
            field=models.TextField(default='failed'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='success_message',
            field=models.TextField(default='win'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='time_limit',
            field=models.TimeField(default=datetime.datetime(2018, 8, 30, 17, 5, 19, 172183, tzinfo=utc)),
            preserve_default=False,
        ),
    ]