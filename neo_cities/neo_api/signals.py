from django.db.models.signals import post_save
from django.dispatch import receiver
from neo_api.models import Action, ResourceEventState, ChatSession, Message
from neo_api.serializers import get_model_serializer, get_resource_event_state, MessageSerializer, ResourceEventStateSerializer, ChatSessionSerializer
from . import dynamic_consumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from neo_api.views import item_data

# TODO Before hook to check that no session is active. If the session is active deny saving

@receiver(post_save, sender=Action)
def send_dynamic_information(**kwargs):
    if kwargs["created"]:
        event = kwargs['instance'].event
        resource = kwargs['instance'].resource
        session = kwargs['instance'].session

        resource_event_state = get_resource_event_state(event, resource, session, kwargs['instance'].participant.role)

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
        channel_layer = get_channel_layer()
        for res in ResourceEventState.objects.filter(session=session):
            response = {
                "item": ResourceEventStateSerializer(res).data,
                "itemId": res.id,
            }
            response["item"]["status"] = win_status
            updated_state = {
                "type": "RES_ITEMS_UPDATE",
                "payload": response                
            }
            updated_state["payload"] = response
            async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": json.dumps(updated_state)})

@receiver(post_save, sender=Message)
def update_chat(**kwargs):
    channel_layer = get_channel_layer()
    message = kwargs["instance"]
    response = {
        "item": get_model_serializer(Message, [])(message).data,
        "itemId": message.id,
        "itemIndex": message.id
    }
    async_to_sync(channel_layer.group_send)("participants", {"type": "send.json","text": json.dumps({"type": "CHAT_ITEMS_ADD", "payload": response})})

# Need to account for Order
# If an event is completed it should remove all the things deployed to it and remain completed
def check_for_win(event, session):
    event_won = True
    thresholds = event.threshold_set.all()
    resource_event_states_time = []
    resource_event_states = []
    # Check that each threshold is met
    for threshold in event.threshold_set.all():
        resource_event_state = ResourceEventState.objects.get(session = session, event = event, resource = threshold.resource)
        print(resource_event_state.deployed, threshold.amount)
        if resource_event_state and resource_event_state.deployed >= threshold.amount:
            resource_event_states.append(resource_event_state)
            resource_event_states_time.append(resource_event_state.updated)
        else:
            # resource_event_state.success = False
            # resource_event_state.save()
            event_won = False

    # If order is enforced and the resource event state updated times aren't in order the order sent is incorrect
    if(thresholds.first().enforce_order and resource_event_states_time != sorted(resource_event_states_time)):
        event_won = False

    if(event_won):
        ResourceEventState.objects.filter(session = session, event = event).update(success = True, deployed = 0)


    return(event_won)
