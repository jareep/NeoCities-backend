from django.shortcuts import render
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action, ResourceEventState, Message, ChatSession
from neo_api.serializers import get_model_serializer, ParticipantSerializer, MessageSerializer, ResourceSerializer, RoleSerializer, ScenarioSerializer , ChatSessionSerializer, ActionSerializer, ResourceEventStateSerializer, get_resource_event_state
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from neo_api import tasks as task
from datetime import datetime  
from datetime import timedelta 
from . import dynamic_consumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# These are field exceptions for every model serializer
field_exceptions = ["scenario", "action"]  # todo: look into storing the Model instead of string

def item_data(model, data, excluded = []):
    response = {
            "items": {},
            "itemsOrder": []
        }
    for item in data:
        response["items"][item.id] =  get_model_serializer(model, excluded)(item).data
        response["itemsOrder"].append(item.id)
    return(response)

def schedule_tasks(session):
    # Go through the events in the scenario and use their time in relation to now 
    # to schedule when they send and remove
    print(session.scenario_ran)
    for event in session.scenario_ran.events.all():
        task.send_event(event.id, schedule = event.start_time)
        task.send_event_failure(event.id, schedule = event.end_time)

    # Go through the briefings in the scenario and use their time in relation to now
    # to schedule when they send and remove
    # for briefing in session.scenario_ran.briefings.all():
    #     task.send_briefing(briefing.id, 10)

class StartSimulation(APIView):

    def get(self, request, sessionKey, format=None):
        session = Session.objects.get(sessionKey = sessionKey)
        # Save the start time on the session
        session.start_time = datetime.now()
        schedule_tasks(session)
        response = {
            "type": "SIMULATED_TIMER_CREATE",
            "payload": {
                "timeStart": session.start_time.timestamp(),
                "simulatedTimeSpeed": 3
            }

        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": json.dumps(response)})
        return(Response({"Simulation": "Started :)"}))


# View for the intial login
class InitParticipant(APIView):
    def get(self, request, participantKey, format=None):
        participant = Participant.objects.get(token = participantKey)
        for resource in participant.role.resources.all():
            for event in participant.session.scenario_ran.events.all():
                get_resource_event_state(event, resource, participant.session, participant.role)
        response = {
            "sessionKey": participant.session.sessionKey,
            "userID": participant.id,
            "chatSessions": participant.chat_session.id,
            "roleID": participant.role.id
        }
        return(Response(response))

class ResourceEventStateViewSet(APIView):

    def get(self, request, sessionKey, format=None):
        session = Session.objects.get(sessionKey = sessionKey)
        current_state = ResourceEventState.objects.filter(session=session)
        return(Response(item_data(ResourceEventState, current_state, field_exceptions)))



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

class ResourceDepotItemView(APIView):
    def get(self, request, sessionKey, format=None):
        role_ids = [role for role in Session.objects.get(sessionKey = sessionKey).scenario_ran.roles.all()]
        resourcedepots = ResourceDepot.objects.filter(role__in = role_ids)
        return(Response(item_data(ResourceDepot, resourcedepots, [])))



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


class RoleItemView(APIView):

    def get(self, request, sessionKey, format=None):
        roles = Session.objects.get(sessionKey = sessionKey).scenario_ran.roles.all()
        return(Response(item_data(Role, roles, ["resourcedepot", "scenario", "briefing", "participant", "resourceeventstate"])))


class MessageItemView(APIView):

    def get(self, request, chatSessionId, format=None):
        chat_session = ChatSession.objects.get(id = chatSessionId)
        messages = Message.objects.filter(chat_session = chat_session)
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
