from django.contrib import admin
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action, ResourceEventState

# Register your models here.
model_list = [Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action, ResourceEventState]
for model in model_list:
    admin.site.register(model)
