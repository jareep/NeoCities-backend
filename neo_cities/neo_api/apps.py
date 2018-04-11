from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver

class NeoApiConfig(AppConfig):
    name = 'neo_api'

    def ready(self):
        print("ready")
        import neo_api.signals
        post_save.connect(receiver, sender='neo_api.Action')
