# Generated by Django 2.0 on 2018-07-16 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neo_api', '0009_auto_20180712_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceeventstate',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='neo_api.Role'),
            preserve_default=False,
        ),
    ]
