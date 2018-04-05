from django.shortcuts import render
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action
from neo_api.serializers import get_model_serializer, ParticipantSerializer, ResourceSerializer, RoleSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
# These are field exceptions for every model serializer
field_exceptions = ["scenario", "action"]  # todo: look into storing the Model instead of string


# View for the intial login
class InitParticipant(APIView):
    def get(self, request, format=None):
        print(request)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = get_model_serializer(Event, field_exceptions + ["threshold"])


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ThresholdViewSet(viewsets.ModelViewSet):
    queryset = Threshold.objects.all()
    serializer_class = get_model_serializer(Threshold, field_exceptions)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ResourceDepotViewSet(viewsets.ModelViewSet):
    queryset = ResourceDepot.objects.all()
    serializer_class = get_model_serializer(ResourceDepot, field_exceptions)


class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = get_model_serializer(Scenario, field_exceptions + ["briefing", "session"])


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = get_model_serializer(Score, field_exceptions + ["participant"])


class BriefingViewSet(viewsets.ModelViewSet):
    queryset = Briefing.objects.all()
    serializer_class = get_model_serializer(Briefing, ["action"])



class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer



class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = get_model_serializer(Session, field_exceptions + ["participant"])



class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = get_model_serializer(Action, field_exceptions + ["threshold", "event", "role", "resourcedepot"])
