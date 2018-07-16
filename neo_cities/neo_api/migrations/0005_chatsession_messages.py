# Generated by Django 2.0 on 2018-06-29 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neo_api', '0004_auto_20180411_0718'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='neo_api.Session')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('chat_session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neo_api.ChatSession')),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neo_api.Participant')),
            ],
        ),
    ]