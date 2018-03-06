from django.shortcuts import render
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action
from neo_api.serializers import get_model_serializer
from rest_framework import viewsets

# These are field exceptions for every model serializer
field_exceptions = ["scenario", "action"]  # todo: look into storing the Model instead of string


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = get_model_serializer(Event, field_exceptions + ["threshold"])


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = get_model_serializer(Resource, field_exceptions + ["threshold", "event", "role", "resourcedepot"])


class ThresholdViewSet(viewsets.ModelViewSet):
    queryset = Threshold.objects.all()
    serializer_class = get_model_serializer(Threshold, field_exceptions + ["threshold", "event", "role", "resourcedepot"])


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = get_model_serializer(Role, field_exceptions + ["threshold", "event", "role", "resourcedepot"])


class ResourceDepotViewSet(viewsets.ModelViewSet):
    queryset = ResourceDepot.objects.all()
    serializer_class = get_model_serializer(ResourceDepot, field_exceptions + ["threshold", "event", "role", "resourcedepot"])


class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = get_model_serializer(Scenario, field_exceptions + ["threshold", "event", "role", "resourcedepot"])


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = get_model_serializer(Score, field_exceptions + ["threshold", "event", "role", "resourcedepot"])


class BriefingViewSet(viewsets.ModelViewSet):
    queryset = Briefing.objects.all()
    serializer_class = get_model_serializer(Briefing, field_exceptions + ["threshold", "event", "role", "resourcedepot"])



class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = get_model_serializer(Participant, field_exceptions + ["threshold", "event", "role", "resourcedepot"])



class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = get_model_serializer(Session, field_exceptions + ["threshold", "event", "role", "resourcedepot"])



class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = get_model_serializer(Action, field_exceptions + ["threshold", "event", "role", "resourcedepot"])
