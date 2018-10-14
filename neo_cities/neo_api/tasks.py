from background_task import background
from django.contrib.auth.models import User
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action, ResourceEventState, Message, ChatSession
from neo_api import views as views
import json
from . import dynamic_consumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime  

# Send new event
@background(schedule=60)
def send_event(event_id):
    # Send the event data through the websocket
    event = Event.objects.filter(id = event_id)
    updated_state = views.item_data(Event, event, ["threshold", "scenario", "action", "resourceeventstate"])
    updated_state["action"] = "Event_Item_Add"
    updated_state["timestamp"] = datetime.now().timestamp()
    updated_state = json.dumps(updated_state)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": updated_state})


# Send event failure
@background(schedule=60)
def send_event_failure(event_id):
    # Send the event data through the websocket
    event = Event.objects.filter(id = event_id)
    updated_state = views.item_data(Event, event, ["threshold", "scenario", "action", "resourceeventstate"])
    updated_state["action"] = "Event_Item_Remove"
    updated_state["timestamp"] = datetime.now().timestamp()
    updated_state = json.dumps(updated_state)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": updated_state})



# Send briefing
@background(schedule=60)
def send_briefing(briefing_id):
    # Send the event data through the websocket
    briefing = Briefing.objects.filter(id = briefing_id)
    updated_state = views.item_data(Briefing, briefing, ["threshold", "scenario", "action", "resourceeventstate"])
    updated_state["action"] = "Briefing_Item_Add"
    updated_state = json.dumps(updated_state)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": updated_state})


# Remove briefing

