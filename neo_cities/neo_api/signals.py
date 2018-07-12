from django.db.models.signals import post_save
from django.dispatch import receiver
from neo_api.models import Action, ResourceEventState, ChatSession, Message
from neo_api.serializers import get_model_serializer, get_resource_event_state, ChatSessionSerializer
from . import dynamic_consumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# TODO Before hook to check that no session is active. If the session is active deny saving

@receiver(post_save, sender=Action)
def send_dynamic_information(**kwargs):
    if kwargs["created"]:
        event = kwargs['instance'].event
        resource = kwargs['instance'].resource
        session = kwargs['instance'].session

        resource_event_state = get_resource_event_state(event, resource, session)

        # Calculate the appropriate values for the ResourceEventState
        print(kwargs['instance'].action_type)
        if(kwargs['instance'].action_type == "DEPLOY"):
            resource_event_state.deployed += kwargs['instance'].quantity
        elif(kwargs['instance'].action_type == "RECALL"):
            resource_event_state.deployed -= kwargs['instance'].quantity
        resource_event_state.save()
        # TODO If Ordering Check the ordering of the ResourceEventState based on the Create TimeStamp
        # Check the Threshold model for the Event and see if the Event was successful
        win_status = check_for_win(event, session)

        # Send the updated ResourceEventState
        async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": json.dumps({ "event_success": win_status, "resource_event_state": get_model_serializer(ResourceEventState, [])(ResourceEventState.objects.filter(session=session), many=True).data})})

@receiver(post_save, sender=Message)
def update_chat(**kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": json.dumps({"ChatSession": get_model_serializer(ChatSession, ["participant", "message"])(kwargs["instance"]).data})})

def check_for_win(event, session):
    event_won = True
    for threshold in event.threshold_set.all():
        resource_event_state = ResourceEventState.objects.get(session = session, event = event, resource = threshold.resource)
        if resource_event_state and resource_event_state.deployed >= threshold.amount:
            resource_event_state.success = True
            resource_event_state.save()
        else:
            resource_event_state.success = False
            resource_event_state.save()
            event_won = False
    return(event_won)
