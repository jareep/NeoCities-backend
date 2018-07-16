from django.shortcuts import render
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action, ResourceEventState, Message, ChatSession
from neo_api.serializers import get_model_serializer, ParticipantSerializer, MessageSerializer, ResourceSerializer, RoleSerializer, ScenarioSerializer , ChatSessionSerializer, ActionSerializer, ResourceEventStateSerializer, get_resource_event_state
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

# These are field exceptions for every model serializer
field_exceptions = ["scenario", "action"]  # todo: look into storing the Model instead of string

def intial_data(participant):
    return({
    "participant": participant.id, "sessionToken": participant.session.sessionKey,
    "sessionID": participant.session.id,
    "ResourceEventStates": ResourceEventStateSerializer(ResourceEventState.objects.filter(session=participant.session), many=True).data,
    "Events": get_model_serializer(Event, field_exceptions + ["threshold", "resourceeventstate"])(participant.session.scenario_ran.events.all(), many=True).data,
    "Briefing": get_model_serializer(Briefing, [])(Briefing.objects.filter(role = participant.role, scenario = participant.session.scenario_ran), many=True).data,
    "ChatSession": ChatSessionSerializer(participant.chat_session).data
    })

# View for the intial login
class InitParticipant(APIView):
    def get(self, request, participantKey, format=None):
        participant = Participant.objects.get(token = participantKey)
        for resource in participant.role.resources.all():
            for event in participant.session.scenario_ran.events.all():
                get_resource_event_state(event, resource, participant.session)
        return(Response(intial_data(participant)))

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


class BriefingViewSet(viewsets.ModelViewSet):
    queryset = Briefing.objects.all()
    serializer_class = get_model_serializer(Briefing, ["action"])



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
