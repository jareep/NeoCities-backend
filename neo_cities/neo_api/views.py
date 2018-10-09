from django.shortcuts import render
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action, ResourceEventState, Message, ChatSession
from neo_api.serializers import get_model_serializer, ParticipantSerializer, MessageSerializer, ResourceSerializer, RoleSerializer, ScenarioSerializer , ChatSessionSerializer, ActionSerializer, ResourceEventStateSerializer, get_resource_event_state
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

# These are field exceptions for every model serializer
field_exceptions = ["scenario", "action"]  # todo: look into storing the Model instead of string

def item_data(model, data, excluded = []):
    response = {
            "items": [],
            "itemsOrder": []
        }
    for item in data:
        response["items"].append({item.id: get_model_serializer(model, excluded)(item).data})
        response["itemsOrder"].append(item.id)
    return(response)

# View for the intial login
class InitParticipant(APIView):
    def get(self, request, participantKey, format=None):
        participant = Participant.objects.get(token = participantKey)
        response = {
            "sessionKey": participant.session.sessionKey,
            "userID": participant.id
        }
        return(Response(response))

class ResourceEventStateViewSet(APIView):

    def get(self, request, sessionKey, format=None):
        session = Session.objects.get(sessionKey = sessionKey)
        current_state = get_model_serializer(ResourceEventState, field_exceptions)(ResourceEventState.objects.filter(session=session), many=True)
        return(Response(current_state.data))



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = get_model_serializer(Event, field_exceptions + ["threshold", "resourceeventstate"])


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


class BriefingItemView(APIView):

    def get(self, request, sessionKey, format=None):
        scenario = Session.objects.get(sessionKey = sessionKey).scenario_ran
        briefings = Briefing.objects.filter(scenario_id = scenario.id)
        return(Response(item_data(Briefing, briefings)))

class EventItemView(APIView):

    def get(self, request, sessionKey, format=None):
        scenario = Session.objects.get(sessionKey = sessionKey).scenario_ran
        events = Event.objects.filter(scenario = scenario)
        return(Response(item_data(Event, events, ["threshold", "scenario", "action", "resourceeventstate"])))

class ResourceItemView(APIView):

    def get(self, request, sessionKey, format=None):
        role_ids = [role for role in Session.objects.get(sessionKey = sessionKey).scenario_ran.roles.all()]
        resources = Resource.objects.filter(role__in = role_ids)
        return(Response(item_data(Resource, resources, ["event", "threshold", "action", "role", "resourcedepot", "resourceeventstate"])))

class MessageItemView(APIView):

    def get(self, request, participantKey, format=None):
        participant = Participant.objects.get(token = participantKey)
        messages = Message.objects.filter(participant_id = participant.id)
        return(Response(item_data(Message, messages)))

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = get_model_serializer(Session, field_exceptions + ["participant", "resourceeventstate", "chatsession"])



class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
