# Generated by Django 2.0 on 2018-07-16 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neo_api', '0010_resourceeventstate_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='threshold',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='resourceeventstate',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
